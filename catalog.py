from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import make_response, flash
from flask import session as login_session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from database_setup import Base, User, CarType, Model

import httplib2
import json
import requests
import random
import string

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)

engine = create_engine('sqlite:///carTypes.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    print data['email']
    if session.query(User).filter_by(email=data['email']).count() != 0:
        current_user = session.query(User).filter_by(email=data['email']).one()
    else:
        newUser = User(name=data['name'],
                       email=data['email'])
        session.add(newUser)
        session.commit()
        current_user = newUser

    login_session['user_id'] = current_user.id
    print current_user.id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None, headers={'content-type': 'application/x-www-form-urlencoded'})[0]

    print url
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successfully logged out")
        return redirect('/cartype')
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/')
@app.route('/cartype')
def showCarType():
    # Show all Car Types
    carTypes = session.query(CarType).all()
    return render_template('category.html', carTypes=carTypes)


@app.route('/cartype/new/', methods=['GET', 'POST'])
def newCarType():
    # Add new Car Type
    if 'username' not in login_session:
        return redirect('/login')

    user_id = login_session['user_id']

    if request.method == 'POST':
        newCarType = CarType(name=request.form['name'], user_id=user_id)
        session.add(newCarType)
        flash('New Car Type %s Successfully Created' % newCarType.name)
        session.commit()
        return redirect(url_for('showCarType'))
    else:
        return render_template('category_new.html')


@app.route('/cartype/<int:carType_id>/edit/', methods=['GET', 'POST'])
def editCarType(carType_id):
    # Edit exsisting Car Type
    if 'username' not in login_session:
        return redirect('/login')

    carType = session.query(CarType).filter_by(id=carType_id).one()

    if carType.user_id != login_session['user_id'] :
        flash('Car Type was created by another user and can only be edited by creator')
        return redirect(url_for('showCarType'))

    if request.method == 'POST':
        if request.form['name']:
            carType.name = request.form['name']
            flash('Car Type Successfully Updated %s' % carType.name)
            return redirect(url_for('showCarType'))
    else:
        return render_template('category_edit.html', carType=carType)


@app.route('/cartype/<int:carType_id>/delete/', methods=['GET', 'POST'])
def deleteCarType(carType_id):
    #  Delete an exsisting Car Type
    if 'username' not in login_session:
        return redirect('/login')

    carType = session.query(CarType).filter_by(id=carType_id).one()

    if carType.user_id != login_session['user_id'] :
        flash('Car Type was created by another user and can only be edited by creator')
        return redirect(url_for('showCarType'))

    if request.method == 'POST':
        session.delete(deleteCarType)
        session.commit()

        flash('%s Successfully Deleted' % carType.name)

        return redirect(url_for('showCarType', carType_id=carType_id))
    else:
        return render_template('category_delete.html', carType=carType)


@app.route('/cartype/<int:carType_id>/')
@app.route('/cartype/<int:carType_id>/item/')
def showModel(carType_id):
    # Show all Car Models
    carType = session.query(CarType).filter_by(id=carType_id).one()
    models = session.query(Model).filter_by(
        carType_id=carType_id).all()
    return render_template('item.html', models=models, carType=carType)


@app.route('/cartype/<int:carType_id>/item/new', methods=['GET', 'POST'])
def newModel(carType_id):
    # Add new Car Model
    if 'username' not in login_session:
        return redirect('/login')

    user_id = login_session['user_id']

    if request.method == 'POST':
        newModel = Model(name=request.form['name'],
                       description=request.form['description'],
                       carType_id=carType_id,
                       user_id=user_id)
        session.add(newModel)
        session.commit()
        flash('%s Successfully Created' % (newModel.name))
        return redirect(url_for('showModel', carType_id=carType_id))
    else:
        return render_template('item_new.html', carType_id=carType_id)

    return render_template('item_new.html', carType_id=carType_id)


@app.route('/cartype/<int:carType_id>/item/<int:model_id>/edit',
           methods=['GET', 'POST'])
def editModel(carType_id, model_id):
    # Edit exsisting Car Model
    if 'username' not in login_session:
        return redirect('/login')

    model = session.query(Model).filter_by(id=model_id).one()

    if model.user_id != login_session['user_id']:
        flash('Model was created by another user and can only be edited by creator')
        return redirect(url_for('showModel', carType_id=carType_id))

    if request.method == 'POST':
        if request.form['name']:
            model.name = request.form['name']
        if request.form['description']:
            model.description = request.form['description']
        session.add(model)
        session.commit()
        flash('%s Successfully Updated' % (model.name))
        return redirect(url_for('showModel', carType_id=carType_id))
    else:
        return render_template('item_edit.html',
                               carType_id=carType_id,
                               model_id=model_id,
                               model=model)


@app.route('/cartype/<int:carType_id>/item/<int:model_id>/delete',
           methods=['GET', 'POST'])
def deleteModel(carType_id, model_id):
    # Delete an exsisting Car Model
    if 'username' not in login_session:
        return redirect('/login')

    model = session.query(Model).filter_by(id=model_id).one()

    if model.user_id != login_session['user_id']:
        flash('Model was created by another user and can only be edited by creator')
        return redirect(url_for('showModel', carType_id=carType_id))

    if request.method == 'POST':
        session.delete(model)
        session.commit()
        flash('%s Successfully Deleted' % (model.name))
        return redirect(url_for('showModel', carType_id=carType_id))
    else:
        return render_template('item_delete.html',
                               carType_id=carType_id,
                               model=model)


@app.route('/cartype/JSON')
def carTypesJSON():
    # Return JSON for all the Car Types
    carTypes = session.query(CarType).all()
    return jsonify(carTypes=[c.serialize for c in carTypes])


@app.route('/cartype/<int:carType_id>/JSON')
def carTypeJSON(carType_id):
    # Return JSON of all the Models for a Car Type
    carType = session.query(CarType).filter_by(id=carType_id).one()
    models = session.query(Model).filter_by(
        carType_id=carType_id).all()
    return jsonify(models=[i.serialize for i in models])

@app.route('/item/JSON')
def modelsJSON():
    # Return JSON for all Car Models
    models = session.query(Model).all()
    return jsonify(models=[i.serialize for i in models])

@app.route('/cartype/<int:carType_id>/item/<int:model_id>/JSON')
def modelJSON(carType_id, model_id):
    # Return JSON for a Car Model
    model = session.query(Model).filter_by(id=model_id).one()
    return jsonify(model=model.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
