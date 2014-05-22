from flask import Flask

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

# with app.app_context():
#     initdb_command()