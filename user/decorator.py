from functools import wraps
from flask import redirect, session, url_for, abort
from user.models import Items

def login_required(f):

	@wraps(f)
	def wrapper(*args, **kwargs):

		if 'email' not in session:

			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return wrapper


def is_author(f):

	@wraps(f)
	def wrapper(*args, **kwargs):

		item = Items.query.filter_by(item=kwargs['iname']).first()

		if 'email' in session:
			if session['email'] != item.email:
				return abort(403, "Don't try this at home!!")

		return f(*args, **kwargs)
	return wrapper
