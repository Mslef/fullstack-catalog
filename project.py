from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, session as login_session
app = Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

from db_setup import Category, Base, Item, User


CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Basic routes to display all categories, a category and an item
@app.route('/')
@app.route('/categories/')
def categoryList():
    category = session.query(Category).all()
    return render_template('index.html', category = category)

@app.route('/categories/<int:category_id>/')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    creator = getUserInfo(category.user_id)
    items = session.query(Item).filter_by(category_id=category.id)
    return render_template('category.html', category = category, items = items)

@app.route('/categories/<int:category_id>/<int:item_id>')
def showItem(category_id, item_id):
    item = session.query(Item).filter_by(category_id=category_id, id=item_id).one()
    creator = getUserInfo(item.user_id)
    return render_template('item.html', item = item)



# Routes for JSON endpoints
@app.route('/categories/<int:category_id>/JSON')
def JSONShowCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id)
    return jsonify(Item=[i.serialize for i in items])

@app.route('/categories/JSON')
def JSONCategoryList():
    category = session.query(Category).all()
    return jsonify(Category=[i.serialize for i in category])

@app.route('/categories/<int:category_id>/<int:item_id>/JSON')
def JSONShowItem(category_id, item_id):
    item = session.query(Item).filter_by(category_id=category_id, id=item_id).one()
    return jsonify(Item=[item.serialize])


#User methods
def createUser(login_session):
    newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
    session.add(newUser)
    session.commit
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user=session.query(User).filter_by(id = user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email)
        return user.id
    except:
        return None

#Create, Edit, and Delete methods for catalog and items
#Categories
@app.route('/categories/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        flash("Please login to create a new Category")
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(name = request.form['name'], user_id = login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash(newCategory.name + " successfully created")
        return redirect('/categories')
    else:
        return render_template('newcategory.html')

@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    creator = getUserInfo(category_id)

    if 'username' not in login_session:
        return redirect('/login')
    if login_session["email"] != creator.email:
        flash("You don't have the permission to edit this category")
        return redirect ("/categories")
    else:
        category = session.query(Category).filter_by(id=category_id).one()
        if request.method == 'POST':
            category.name = request.form['name']
            session.commit()
            flash(category.name + " successfully edited")
            return redirect('/categories')
        else :
            return render_template('editcategory.html', category = category)

@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')

    if login_session["email"] != creator.email:
        flash("You don't have the permission to delete this category")
        return redirect ("/categories")
    else:
        category = session.query(Category).filter_by(id=category_id).one()
        if request.method == 'POST':
            session.delete(category)
            session.commit
            flash(category.name + " successfully deleted")
            return redirect('/categories')

        else:
            return render_template('deletecategory.html', category = category)


#Items
@app.route('/categories/<int:category_id>/new/', methods=['GET', 'POST'])
def newItem(category_id):

    if 'username' not in login_session:
        flash("Please login to create a new item")
        return redirect('/login')

    if request.method == 'POST':
        newItem = Item(name = request.form['name'], description=request.form['description'], image_url = request.form['url'], category_id = category_id, user_id = login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash(newItem.name + " successfully added")
        return redirect(url_for('showCategory', category_id = category_id))
    else:
        category = session.query(Category).filter_by(id=category_id).one()
        return render_template('newitem.html', category = category)

@app.route('/categories/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    creator = getUserInfo(category_id)

    if 'username' not in login_session:
        return redirect('/login')

    if login_session["email"] != creator.email:
        flash("You don't have the permission to edit this item")
        return redirect(url_for('showCategory', category_id = category_id))

    item = session.query(Item).filter_by(category_id=category_id, id=item_id).one()
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.image_url = request.form['url']
        session.commit()
        flash(item.name + ' successfully edited')
        return redirect(url_for('showCategory', category_id = category_id))
    else:
        return render_template('edititem.html', item = item)

@app.route('/categories/<int:category_id>/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    creator = getUserInfo(category_id)

    if 'username' not in login_session:
        return redirect('/login')

    if login_session["email"] != creator.email:
        flash("You don't have the permission to delete this item")
        return redirect(url_for('showCategory', category_id = category_id))

    item = session.query(Item).filter_by(category_id=category_id, id=item_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash(item.name + ' successfully deleted')
        return redirect(url_for('showCategory', category_id = category_id))
    else:
        return render_template('deleteitem.html', item = item)

#Login page
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Function to return a response following a request
def return_response(response_string, response_code):
    response = make_response(json.dumps(response_string), response_code)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Compare the state in the url returned from the site
    # to the state in the server-side login-session to protect against CSFA
    if request.args.get('state') != login_session['state']:
        return_response('Invalid state parameter', 401)

    # If the states match, get the one-time code from the server
    code = request.data
    # Try to use one-time code to get credentials
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError :
        return_response('Failed to upgrade authorization code.', 401)

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # Abort if error in the access token info
    if result.get('error') is not None:
        response = return_response(result.get('error'), 501)

    # Validate user ID and client ID
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return_response("Token's user ID doesn't match given user ID.", 401)

    if result['issued_to'] != CLIENT_ID:
        print "Token's client ID doesn't match app's."
        return_response("Token's client ID doesn't match app's.", 401)

    #Check if user already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = return_response("Current user is already connected", 200)
        return "You are already logged in as %s!" %login_session['username']

    #Store the access token in the session for later use
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    #Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params = params)

    data = json.loads(answer.text)

    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    #Get the user ID from the db
    login_session['user_id'] = user_id

    #Output a welcome message
    output = "<h1> Welcome, %s !</h1>" % login_session['username']
    output+= "<img src='%s' style='width: 300px; height:300px;'>"% login_session['picture']
    flash ("you are now logged in as %s"%login_session['username'])
    return output

@app.route("/gdisconnect")
def gdisconnect():
    #Check if user is connected
    access_token = login_session.get("access_token")
    if access_token is not None:
        return_response('Current user not connected.', 401)

    #Execute HTTP GET request to revoque current token
    url = ('https://www.accounts.google.com/o/oauth2/revoke?token=%s'
           % access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == 200:
        #Reset the user's session.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        return_response('Successfully disconnected.', 200)
    else:
        return_response('Failed to revoke the token for given user.', 400)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '127.0.0.1', port = 8080)
