from catalog import app, photos, db
from flask import render_template, redirect, request, session as login_session, flash, url_for, make_response, jsonify, abort  # NOQA
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import random
import string
import requests
from user.forms import AddItem
from user.models import Items
from user.decorator import login_required, is_author


CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']  # NOQA

@app.route('/')
@app.route('/home')
def home():
    ''' This function renders the home page listing all the latest items '''

    items = Items.query.order_by(Items.id.desc()).limit(4).all()
    sports = len(Items.query.filter_by(category='Sports').all())
    electronics = len(Items.query.filter_by(category='Electronics').all())
    books = len(Items.query.filter_by(category='Books').all())
    mobiles = len(Items.query.filter_by(category='Mobiles').all())
    skincare = len(Items.query.filter_by(category='Skincare').all())
    accessories = len(Items.query.filter_by(category='Accessories').all())
    gifts = len(Items.query.filter_by(category='Gift items').all())
    shoes = len(Items.query.filter_by(category='Shoes').all())

    return render_template('home.html', items=items,
                                        sports=sports,
                                        electronics=electronics,
                                        books=books,
                                        mobiles=mobiles,
                                        skincare=skincare,
                                        accessories=accessories,
                                        gifts=gifts,
                                        shoes=shoes)


@app.route('/login')
def login():
    ''' This function renders the login page and authenticates the user '''

    state = ''.join(random.choice(string.ascii_uppercase+string.digits) 
            for x in range(32))

    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    ''' This is a callback function responsible to authenticate 
        and authorize the user via Google api.  '''

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
    result = json.loads((h.request(url, 'GET')[1]).decode('utf-8'))
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
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Already connected.'),
                                 200)
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


    flash("You are now logged in as %s" % login_session['username'])
    return '<h6>Redirecting...</h6>'


@app.route('/logout')
@login_required
def logout():
    ''' This function logs out the user, deletes the cookies 
        and redirects to the home page. '''

    login_session.pop('email')
    login_session.pop('picture')
    login_session.pop('username')
    login_session.pop('access_token')
    login_session.pop('gplus_id')

    flash('You have been successfully logged out.')
    return redirect(url_for('home'))


@app.route('/category/<name>')
def category(name):
    ''' This function renders all the items from a specific 
        category visited by the user '''

    items = Items.query.filter_by(category=name).all()
    sports = len(Items.query.filter_by(category='Sports').all())
    electronics = len(Items.query.filter_by(category='Electronics').all())
    books = len(Items.query.filter_by(category='Books').all())
    mobiles = len(Items.query.filter_by(category='Mobiles').all())
    skincare = len(Items.query.filter_by(category='Skincare').all())
    accessories = len(Items.query.filter_by(category='Accessories').all())
    gifts = len(Items.query.filter_by(category='Gift items').all())
    shoes = len(Items.query.filter_by(category='Shoes').all())

    return render_template('category.html', name=name, items=items,
                                            sports=sports,
                                            electronics=electronics,
                                            books=books,
                                            mobiles=mobiles,
                                            skincare=skincare,
                                            accessories=accessories,
                                            gifts=gifts,
                                            shoes=shoes)


@app.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    ''' This function adds a new item to the database and 
        displays them into the given category '''


    form = AddItem()
    # Validating the form submission
    if form.validate_on_submit():
        # Uploading image if any.
        filename = None
        try:
            filename = photos.save(request.files['image'])
        except:
            pass
        # If not image was uploaded then assigning to default image
        if not filename:
            filename = 'default-image.jpg'
        # Storing all the item info's for creating the instance of the table.
        email = login_session['email']
        item_name = form.item_name.data
        description = form.description.data
        category = form.category.data
        price = form.price.data
        # Creating the instance of the table and 
        # commiting the changes to the database.
        item = Items(email, item_name, 
                    description, filename, 
                    category, price)

        db.session.add(item)
        db.session.commit()
        flash(item_name + ' has been successfully added to the list.')

        return redirect(url_for('category', name=category))

    return render_template('add_item.html', form=form)


@app.route('/category/<cname>/<iname>')
def item(cname, iname):
    ''' This function displays a particular item along with 
        all its details from the database '''

    # Stores are all items belonging to the same category
    items = Items.query.filter_by(category=cname).all()
    # Stores the instance the requested item to be displayed
    itm = Items.query.filter_by(item=iname).first()

    return render_template('item.html',
                            items=items,
                            cname=cname,
                            iname=iname,
                            itm=itm)


@app.route('/myitems')
@login_required
def myitems():

    items = []
    user = login_session['email']
    items = Items.query.filter_by(email=user).all()
    total = len(items)

    return render_template('myitems.html', items=items, total=total)

@app.route('/edit/<iname>', methods=['GET', 'POST'])
@login_required
@is_author
def edit(iname):

    item = Items.query.filter_by(item=iname).first()
    filename = None
    form = AddItem(item_name=item.item,
                   description=item.description,
                   image=item.image,
                   category=item.category,
                   price=item.price)

    if form.validate_on_submit():

        item.item = form.item_name.data
        item.description = form.description.data
        try:
            filename = photos.save(request.files['image'])
            item.image = filename
        except:
            pass

        item.category = form.category.data
        item.price = form.price.data

        db.session.add(item)
        db.session.commit()
        flash(iname + ' successfully updated.')
        return redirect(url_for('item', cname=item.category, iname=item.item))

    return render_template('edit.html', iname=iname, form=form)


@app.route('/delete/<iname>')
@login_required
@is_author
def delete(iname):

    item = Items.query.filter_by(item=iname).first()
    cname = item.category
    db.session.delete(item)
    db.session.commit()

    flash(iname + ' successfully deleted.')

    return redirect(url_for('category', name=cname))


@app.route('/api/catalog')
def api():

    items = Items.query.all()

    return jsonify(item=[ i.serialize for i in items])