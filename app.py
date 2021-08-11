"""
This file contains the backend code for Item Catalog Application
"""

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from db_setup import Categories, Base, Items, User

from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from flask import session as login_session

# Imports For Authentication
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response
import requests
import random
import string
import httplib2
import json

app = Flask(__name__)
APPLICATION_NAME = "Item Catalog Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Generic Attributes for Authentication and Authorization
CLIENT_ID = json.loads(open('client_secrets.json', 'r')
                       .read())['web']['client_id']
CLIENT_SECRET = json.loads(open('client_secrets.json', 'r')
                           .read())['web']['client_secret']
app.secret_key = CLIENT_SECRET
state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                for x in range(32))


"""
Below Functions display the home page,
categories and related items before user login.
"""


@app.route('/')
def homePage():
    # check user login state
    user_login = None
    if 'username' in login_session:
        user_login = True
    login_session['state'] = state
    # fetch all the categories
    categories = session.query(Categories).order_by(asc(Categories.name))
    # fetch top 5 newly added items
    latest_addition = session.query(Items).order_by(
        desc(Items.create_date)).limit(5)
    # display page
    return render_template('index.html', categories=categories,
                           latest_addition=latest_addition,
                           STATE=state, user_login=user_login,
                           CLIENT_ID=CLIENT_ID)


@app.route('/<category>')
def showCategory(category):
    # check user login state
    user_login = None
    if 'username' in login_session:
        user_login = True
    state = login_session['state']
    # fetch all the categories
    categories = session.query(Categories).order_by(asc(Categories.name))
    # fetch the selected category
    category = session.query(Categories).filter_by(
        name=category.replace('-', ' ')).first()
    if category:
        # fetch all the items from slected category
        category_items = session.query(Items).filter_by(
            item_category_id=category.id).order_by(asc(Items.name))
        # item count in slected category
        items_count = session.query(Items).filter_by(
            item_category_id=category.id).count()
        # display page
        return render_template('showCategory.html', categories=categories,
                               category_name=category.name,
                               category_items=category_items,
                               items_count=items_count,
                               STATE=state, user_login=user_login,
                               CLIENT_ID=CLIENT_ID)
    else:
        return redirect(url_for('homePage'))


@app.route('/<category>/<item>')
def showItem(category, item):
    # check user login state
    user_login = None
    if 'username' in login_session:
        user_login = True
    state = login_session['state']
    # fetch the selected item's category
    category = session.query(Categories).filter_by(
        name=category.replace('-', ' ')).first()
    # fetch the selected item
    item = session.query(Items).filter_by(name=item.replace(
        '-', ' '), item_category_id=category.id).first()
    # display page
    return render_template('showItem.html', category=category,
                           item=item, STATE=state,
                           user_login=user_login,
                           CLIENT_ID=CLIENT_ID)


"""
Login and user helper functions
"""


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
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'
           .format(access_token))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    guser_id = credentials.id_token['sub']
    print(f"Google User ID is {guser_id}.")
    print(f"Result from Google access token is:, '\n', {result}.")
    if result['user_id'] != guser_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_guser_id = login_session.get('guser_id')
    if stored_access_token is not None and guser_id == stored_guser_id:
        response = make_response(json.dumps('user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['guser_id'] = guser_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']

    login_session['email'] = data['email']

    # if user doesn't exist then create a new one.
    user_id = (session.query(User).filter_by(email=data["email"]).one()).id
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h4>Welcome, '
    output += login_session['username']
    output += '!</h4>'
    return output

# creates a standalone user.


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


"""
Add, Edit and Delete Item functionality allowed after user authentication
"""


@app.route('/add', methods=['GET', 'POST'])
def addItem():
    # check user login state
    user_login = None
    if 'username' in login_session:
        user_login = True
    else:
        flash('Login required to add item.')
        return redirect(url_for('homePage'))
    if request.method == 'POST':
        # Get item details
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        status = request.form['item_status']
        category = request.form['item_category']
        # validate non null fields
        if not request.form['name']:
            flash('Item name is mandatory to add')
            return redirect(url_for('homePage'))
        # fetch selected category
        selected_category = session.query(Categories).filter_by(
            name=category).one()
        # fetch user id from session
        user_id = (session.query(User).filter_by(
            email=login_session['email']).one()).id
        # create and add new item
        new_item = Items(name=name,
                         description=description,
                         price=price,
                         status=status,
                         item_category_id=selected_category.id,
                         user_id=user_id)
        session.add(new_item)
        session.commit()
        flash(f"New Item {new_item.name} created.")
        return redirect(url_for('homePage'))
    else:
        categories = session.query(Categories).all()
        return render_template('addItem.html',
                               categories=categories,
                               user_login=user_login)


@app.route('/<category>/<item>/edit',
           methods=['GET', 'POST'])
def editItem(category, item):
    # check user login state
    user_login = None
    if 'username' in login_session:
        user_login = True
    else:
        flash('Login required to update item.')
        return redirect(url_for('homePage'))

    if request.method == 'POST':
        # fetch item category
        category = session.query(Categories).filter_by(
            name=category).one()
        # fetch item to edit
        item = session.query(Items).filter_by(
            name=item, item_category_id=category.id).one()
        # get item details from edit form
        if request.form['price']:
            price = request.form['price']
        else:
            price = item.price
        if request.form['item_status']:
            status = request.form['item_status']
        else:
            status = item.status
        # fetch user id from session
        current_user_id = (session.query(User).filter_by(
            email=login_session['email']).one()).id
        item_user_id = item.user_id
        if current_user_id != item_user_id:
            flash('You have not created this Item. Edit is not allowed.')
            return redirect(url_for('homePage'))

        # update item
        item.price = price
        item.status = status
        session.add(item)
        session.commit()
        flash(f"Item {item.name} updated succesfully.")
        return redirect(url_for('homePage'))
    else:
        return render_template('editItem.html', user_login=user_login)


@app.route('/<category>/<item>/delete',
           methods=['GET', 'POST'])
def deleteItem(category, item):
    # check user login state
    user_login = None
    if 'username' in login_session:
        user_login = True
    else:
        flash('Login required to delete item.')
        return redirect(url_for('homePage'))

    if request.method == 'POST':
        # fetch item category
        category = session.query(Categories).filter_by(
            name=category).one()
        # fetch item to delete
        item = session.query(Items).filter_by(
            name=item, item_category_id=category.id).one()
        # fetch user id from session
        current_user_id = (session.query(User).filter_by(
            email=login_session['email']).one()).id
        item_user_id = item.user_id
        if current_user_id != item_user_id:
            flash('You have not created this Item. Delete is not allowed.')
            return redirect(url_for('homePage'))
        # delete item
        session.delete(item)
        session.commit()
        flash(f"Item {item.name} deleted succesfully")
        return redirect(url_for('homePage'))
    else:
        return render_template('deleteItem.html',
                               item=item, user_login=user_login)


"""
Json endpoint to dispaly all categories and items
"""


@app.route('/json')
def catalogJson():
    all_categories = session.query(Categories).all()
    all_items = session.query(Items).all()
    return jsonify(categories=([categories.serialize
                                for categories in all_categories]),
                   items=([items.serialize
                           for items in all_items]))


"""
Logout funtionality
"""


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = f"https://accounts.google.com/o/oauth2/revoke?token={access_token}"
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['guser_id']
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        flash("You are successfully logged out.")
        return redirect(url_for('homePage'))
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=False)
