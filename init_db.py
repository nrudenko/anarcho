import sys

import os


if len(sys.argv) >= 2 and sys.argv[1] == 'local':
    os.environ['DATABASE_URL'] = 'sqlite:///anarcho.db'

from app import db, app
from app.models.application import Application
from app.models.build import Build
from app.models.user import User, UserApp
from flask.ext.login import make_secure_token

db.create_all()

with app.app_context():
    username = "admin"
    password = "admin"
    email = "admin@mail.com"
    api_key = make_secure_token(email, username, password)
    user = User(username, password, email, api_key)
    db.session.add(user)
    db.session.commit()

    application = Application("com.package")
    userApp = UserApp(User.query.filter_by(username="admin").first().id, application.app_key)

    build = Build(application.app_key, "11", "1.1", "rn", "http://...")

    db.session.add(application)
    db.session.add(userApp)
    db.session.add(build)
    db.session.commit()
