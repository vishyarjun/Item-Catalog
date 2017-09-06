from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from database_setup import Base, Sales_Category, User_Details, Sales_Item
from flask import session as login_session
import random
import string
from datetime import datetime
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
app = Flask(__name__)

CLIENT_ID = json.loads(
                open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Project Catalog"
engine = create_engine('sqlite:///salescatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create a login page
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Method for connecting third party OAuth - FB
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange
        we have to split the token first on commas and select the first index
        which gives us the key : value for the server access token then we
        split it on colons to pull out the actual token value and replace
        the remaining quotes with nothing so that it can be used directly in
        the graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')
    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]
    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token
    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]
    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = Createuser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' "style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("Now logged in as %s" % login_session['username'])
    return output


# Method for disconnecting third party OAuth - FB
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s'% (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


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
    url = ('https://www.googleapis.com/oauth2/v2/tokeninfo?access_token=%s' % access_token)
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
        response = make_response(json.dumps('Current user is already' +
                                            ' connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = Createuser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

    # DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'% login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given'
                                            + ' user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# this method displays all the car sales items latest at the top
@app.route('/')
@app.route('/sales/')
def categoryItems():
    allcategory = session.query(Sales_Category)
    items = session.query(Sales_Item).order_by(desc(Sales_Item.item_id))
    u_email = login_session.get('email')
    if u_email:
        u_name = getUserID(login_session.get('email'))
        if u_name is None:
            u_email = Createuser(login_session)
    return render_template('index.html',
                           category=None,
                           items=items,
                           allcategory=allcategory,
                           user_email=login_session.get('email'),
                           username=login_session.get('username'),
                           usr_img=login_session.get('picture'))


# this method is used to list all the cars for the selected category
@app.route('/sales/<string:name>')
def selectCategory(name):
    allcategory = session.query(Sales_Category)
    ctg = session.query(Sales_Category).filter_by(name=name).one()
    items = session.query(Sales_Item).filter_by(category_id=ctg.category_id)
    return render_template('index.html',
                           category=ctg,
                           items=items,
                           allcategory=allcategory,
                           user_email=login_session.get('email'),
                           username=login_session.get('username'),
                           usr_img=login_session.get('picture'))


# this method returns a JSON based on structure defined in database_setup.py
@app.route('/sales/<string:name>/JSON')
def selectCategoryJSON(name):
    ctg = session.query(Sales_Category).filter_by(name=name).one()
    items = session.query(Sales_Item).filter_by(category_id=ctg.category_id).all()
    return jsonify(Sales_Item=[i.serialize for i in items])


# method to add a new car for a category
@app.route('/sales/<string:name>/new/', methods=['GET', 'POST'])
def newItem(name):
    category = session.query(Sales_Category).filter_by(name=name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        salesItem = Sales_Item(name=request.form['name'],
                               description=request.form['description'],
                               category_id=category.category_id,
                               price=request.form['price'],
                               created_by=login_session['email'],
                               created_on=datetime.now(),
                               user_email=login_session['email'])
        session.add(salesItem)
        session.commit()
        flash("A new " + name + " item added for sale -" + salesItem.name
              + "!")
        return redirect(url_for('categoryItems'))
    return render_template('add_new_item.html', category=category)


# Method to edit car name, description and price
@app.route('/sales/<string:name>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(name, item_id):
    edited_item = session.query(Sales_Item).filter_by(item_id=item_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        edited_item.name = request.form['name']
        edited_item.description = request.form['description']
        edited_item.price = request.form['price']
        session.add(edited_item)
        session.commit()
        flash("Item " + edited_item.name + " edited succesfully!")
        return redirect(url_for('categoryItems'))
    return render_template('edit_item.html', item=edited_item, cname=name)


# Method to delete a Car from the item list
@app.route('/sales/<string:name>/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def deleteItem(name, item_id):
    delete_item = session.query(Sales_Item).filter_by(item_id=item_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        session.delete(delete_item)
        session.commit()
        flash("Item " + delete_item.name + " deleted succesfully!")
        return redirect(url_for('categoryItems'))

    return render_template('delete_item.html', item=delete_item, cname=name)


# This method is used to create a new user entry in user_details table
def Createuser(login_session):
    newuser = User_Details(user_email=login_session.get('email'),
                           first_name=login_session.get('username'),
                           img=login_session.get('picture'))
    session.add(newuser)
    session.commit()
    return newuser.user_email


# This method is used to retreive user from DB and return user Class
def getUserInfo(user_email):
    user = session.query(User_Details).filter_by(user_email=user_email).one()
    return user


# This method is used to retreive user from DB and return users ID
def getUserID(user_email):
    try:
        user = session.query(User_Details).filter_by(user_email=user_email).one()
        return user.user_email
    except:
        return None


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del gplus_id
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('categoryItems'))
    else:
        flash("You were not logged in")
        return redirect(url_for('categoryItems'))


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
