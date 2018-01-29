DEBUG = True
SECRET_KEY = 'Supersecret'
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://vagrant:vagrant@0.0.0.0/catalog'
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOADED_PHOTOS_DEST = 'catalog/static/images'