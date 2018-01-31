''' This module is a python decorator and handles security of the app '''

from functools import wraps
from flask import redirect, session, url_for, abort
from user.models import Items


def login_required(f):
    ''' This function checks whether a user is logged in before
        allowing them access to restricted pages '''

    @wraps(f)
    def wrapper(*args, **kwargs):

        if 'email' not in session:

            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper


def is_author(f):
    ''' This function allows the user to change the contents of an 
        item only if the current user is the owner of that item. '''

    @wraps(f)
    def wrapper(*args, **kwargs):

        item = Items.query.filter_by(item=kwargs['iname']).first()

        if 'email' in session:
            if session['email'] != item.email:
                return abort(403, "Don't try this at home!!")

        return f(*args, **kwargs)
    return wrapper
