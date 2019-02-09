from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, CarType, Model, User

# Create database and create a shortcut for easier to update database
engine = create_engine('sqlite:///carTypes.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
user1 = User(name="Daniel G", email="dgethner@gmail.com")
session.add(user1)
session.commit()

# Create Car Type of Coupe
carType1 = CarType(user_id=1, name="Coupe")
session.add(carType1)
session.commit()


# Create Car Type of Convertible
carType2 = CarType(user_id=1, name="Convertible")
session.add(carType2)
session.commit()

# Create Car Type of Sedan
carType3 = CarType(user_id=1, name="Sedan")
session.add(carType3)
session.commit()

# Create Car Type of Crossover
carType4 = CarType(user_id=1, name="Crossover")
session.add(carType4)
session.commit()

# Create Car Type of Sport utility vehicle
carType5 = CarType(user_id=1, name="Sport utility vehicle")
session.add(carType5)
session.commit()

# Create Car Type of Hatchback
carType6 = CarType(user_id=1, name="Hatchback")
session.add(carType6)
session.commit()


# Add Models into CarTypes
model1 = Model(user_id=1, name="Ford Mustang",
                             description="Two door vehicle with a sporty design\
                              typically paired with a V8 engine for power, \
                              can be used daily or at the track.",
                             carType=carType1)
session.add(model1)
session.commit()

model2 = Model(user_id=1, name="Lexus RC",
                             description="Two door vehicle with a sporty design\
                              built for luxury and performance, \
                              can be used daily or at the track.",
                             carType=carType1)
session.add(model2)
session.commit()

model3 = Model(user_id=1, name="Mazda MX-5",
                             description="A small well-built convertible\
                              made to handle extremely well, \
                              can be used daily or at the track.",
                             carType=carType2)
session.add(model3)
session.commit()

model4 = Model(user_id=1, name="FIAT 124 Spider",
                             description="A small convertible\
                              low to the ground for better handling, \
                              can be used daily or at the track.",
                             carType=carType2)
session.add(model4)
session.commit()

model5 = Model(user_id=1, name="Ford Fusion",
                             description="A typical communter car\
                              easily handles four passengers, \
                              should be used as a daily driver.",
                             carType=carType3)
session.add(model5)
session.commit()

model6 = Model(user_id=1, name="Subaru Legacy",
                             description="A four door car\
                              built to handle all weather with AWD, \
                              comfortable with a little bit of luxury.",
                             carType=carType3)
session.add(model6)
session.commit()

model7 = Model(user_id=1, name="Ford Escape",
                             description="Built to be slightly larger\
                              than a sedan and smaller than a SUV, \
                              can hold five passengers comfortably.",
                             carType=carType4)
session.add(model7)
session.commit()

model8 = Model(user_id=1, name="Kia Sorento",
                             description="Affordable crossover\
                              with enough trunk space to handle cargo, \
                              can get good fuel economy.",
                             carType=carType4)
session.add(model8)
session.commit()

model9 = Model(user_id=1, name="Acura MDX",
                             description="Luxury SUV with AWD\
                              made to handle all weather in comfort, \
                              combine technology with luxury.",
                             carType=carType5)
session.add(model9)
session.commit()

model10 = Model(user_id=1, name="Audi Q7",
                             description="Sleek German design\
                              drive around looking sporty and stylish, \
                              combine technology with luxury.",
                             carType=carType5)
session.add(model10)
session.commit()

model11 = Model(user_id=1, name="Mazda 3",
                             description="Small hatchback with\
                              plenty of technology equipped, \
                              great handling and affordable.",
                             carType=carType6)
session.add(model11)
session.commit()

model12 = Model(user_id=1, name="Ford Focus",
                             description="Small hatchback with\
                              plenty of room for cargo, \
                              made to look sporty and above average handling.",
                             carType=carType6)
session.add(model12)
session.commit()

print "added category items!"
