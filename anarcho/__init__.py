from anarcho.storage_workers import storage_types
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask import Flask, redirect
from flask.ext.login import LoginManager

app = Flask(__name__, static_url_path="")
login_manager = LoginManager()
login_manager.init_app(app)

import config_module

app.config.from_object(config_module.DefaultConfig)

db = SQLAlchemy(app)

tmp_dir = app.config["TMP_DIR"]
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

logs_dir = app.config["LOGS_DIR"]
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

worker_type = storage_types[app.config["STORAGE_WORKER"]]
storage_worker = worker_type(app)

if not app.debug:
    import logging

    exceptionsHandler = logging.FileHandler(os.path.join(logs_dir, "error.log"))
    exceptionsHandler.setLevel(logging.ERROR)
    app.logger.addHandler(exceptionsHandler)

from anarcho import apps_views, auth, auth_views, tracking_views, team_views


@app.route('/')
def index():
    return app.send_static_file("index.html")


@app.errorhandler(404)
@app.errorhandler(405)
def stub(e):
    return redirect("/404.html")