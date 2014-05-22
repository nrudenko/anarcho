from flask import Flask

app = Flask(__name__)
from app import views

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin',
    UPLOAD_FOLDER='tmp/',
))