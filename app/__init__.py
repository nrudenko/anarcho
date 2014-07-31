from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask import Flask
from flask.ext.login import LoginManager


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config.update(dict(
    SECRET_KEY=os.urandom(24),
    USERNAME='admin',
    PASSWORD='admin',
    UPLOAD_FOLDER='tmp/',
))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

from app import views, auth, api_views, api_auth_views, tracking_views

upload_dir = os.path.abspath(app.config['UPLOAD_FOLDER'])
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)