from flask import Flask
import os
app = Flask(__name__)
from app import views
from app.db_utils import initdb_command

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin',
    UPLOAD_FOLDER='tmp/',
    DATABASE="anarcho.db"
))

with app.app_context():
    """
    initial actions
    """
    upload_dir = os.path.abspath(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    db_file = app.config['DATABASE']
    if not os.path.isfile(db_file):
        initdb_command()
