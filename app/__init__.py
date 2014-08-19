from file_worker import LocalStorageWorker
from flask.ext.sqlalchemy import SQLAlchemy
from flask.templating import render_template
import os
from flask import Flask, redirect
from flask.ext.login import LoginManager

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config.update(dict(
    UPLOAD_FOLDER=os.path.abspath('builds'),
    SECRET_KEY=os.urandom(24),
    USERNAME='admin',
    PASSWORD='admin'
))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

builds_dir = app.config['UPLOAD_FOLDER']
if not os.path.exists(builds_dir):
    os.makedirs(builds_dir)

build_worker = LocalStorageWorker(app)

if not app.debug:
    import logging

    error_handler = logging.StreamHandler()
    error_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(error_handler)

from app import apps_views, auth_views, tracking_views


@app.route('/')
def index():
    return render_template("index.html")


@app.errorhandler(404)
@app.errorhandler(405)
def stub(e):
    return redirect("/")