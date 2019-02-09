import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False, unique=True)
    name = Column(String(250))

    @property
    def serialize(self):
        # Returns user data in easily serializeable format
        return {
            'email': self.email,
            'name': self.name,
            'id': self.id,
        }


class CarType(Base):
    __tablename__ = 'carType'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User)

    @property
    def serialize(self):
        # Returns CarTypes data in easily serializeable format
        return {
            'name': self.name,
            'id': self.id,
            'user_id': self.user_id,
        }


class Model(Base):
    __tablename__ = 'model'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    carType_id = Column(Integer, ForeignKey('carType.id'))
    carType = relationship("CarType", backref=backref("models", cascade="all, delete-orphan"))

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User)

    @property
    def serialize(self):
        # Returns Model data in easily serializeable format
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'user_id':self.user_id,
        }


engine = create_engine('sqlite:///carTypes.db?check_same_thread=False')
Base.metadata.create_all(engine)
