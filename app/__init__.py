import os
from flask import Flask
from flask.ext.login import LoginManager

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

from app import views

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin',
    UPLOAD_FOLDER='tmp/',
    DATABASE="anarcho.db"
))

upload_dir = os.path.abspath(app.config['UPLOAD_FOLDER'])
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)