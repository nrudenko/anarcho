from os.path import expanduser
import os
import uuid

from anarcho.storage_workers import storage_types
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, redirect, request
from flask.ext.login import LoginManager

import logging
from datetime import datetime

def get_default_config_path():
    config_path = os.path.join(expanduser("~"), ".anarcho", "config.py")
    return config_path


app = Flask(__name__, static_url_path="")

app.config.update({
    'AUTO_RELOAD': False,
    'DEBUG': False,
    'SECRET_KEY': str(uuid.uuid4())})

login_manager = LoginManager()
login_manager.init_app(app)

default_config_path = get_default_config_path()
if os.path.exists(default_config_path):
    app.config.from_pyfile(default_config_path)
else:
    raise ValueError("Configuration file does not exist. Use 'anarcho init' to initialize the file.")

db = SQLAlchemy(app)

tmp_dir = app.config["TMP_DIR"]
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

logs_dir = app.config["LOGS_DIR"]
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

app.worker_config = app.config['STORAGE_WORKER']

worker_type = app.worker_config['type']
storage_worker = storage_types[worker_type](app)

access_log_handler = logging.FileHandler(os.path.join(logs_dir, "access.log"))
access_log_handler.setLevel(logging.NOTSET)
app.logger.addHandler(access_log_handler)

@app.before_request
def pre_request_logging():
    app.logger.info('  '.join([
        datetime.today().ctime(),
        request.method,
        request.url
    ])
    )


from anarcho import apps_views, auth, auth_views, tracking_views, team_views


@app.route('/')
def index():
    return app.send_static_file("index.html")


@app.errorhandler(404)
@app.errorhandler(405)
def stub(e):
    return redirect("/404.html")