from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import UploadSet, IMAGES, configure_uploads


app = Flask(__name__)
app.config.from_object('settings')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

from user import views

