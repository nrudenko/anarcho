import time

import os


if 'DATABASE_URL' not in os.environ:
    os.environ['DATABASE_URL'] = 'sqlite:///anarcho.db'

from app import db, app
from app.models.application import Application
from app.models.build import Build
from app.models.user import User, UserApp
from app.models.tracks import Track

db.create_all()

with app.app_context():
    user = User.query.filter_by(username="admin").first()
    # if user is None:
    username = "admin"
    password = "admin"
    email = "admin@mail.com"
    user = User(username, password, email)
    db.session.add(user)
    db.session.commit()

    user = User.query.filter_by(username="admin").first()

    # if user.apps is None:
    application = Application("TestApp")
    print user.to_dict()
    userApp = UserApp(user.id, application.app_key)

    build = Build(application.app_key, "11", "1.1", "rn", "http://...")

    db.session.add(application)
    db.session.add(userApp)

    track = Track('test1', time.time())
    db.session.add(track)

    db.session.commit()


