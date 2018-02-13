''' This module configures the app '''

DEBUG = True
SECRET_KEY = '\x1fR5\xa9\xb9\xee8\x89\x0et{\xbdIp\x01\xe1k\xcdt\x04\xf2\x9d\xac\x0f'
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://grader:grader@0.0.0.0/catalog'
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOADED_PHOTOS_DEST = 'catalog/static/images'
