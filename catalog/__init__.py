from flask import Flask, url_for

app = Flask(__name__)
app.config.from_object('settings')

from user import views

