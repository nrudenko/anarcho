import sys
import time

import os


if len(sys.argv) >= 2 and sys.argv[1] == 'local':
    os.environ['DATABASE_URL'] = 'sqlite:///anarcho.db'

from app import db, app
from app.models.application import Application
from app.models.build import Build
from app.models.user import User, UserApp
from app.models.tracks import Track
from flask.ext.login import make_secure_token

db.create_all()

with app.app_context():
    user = User.query.filter_by(username="admin").first()
    if user is None:
        username = "admin"
        password = "admin"
        email = "admin@mail.com"
        auth_token = make_secure_token(email, username, password)
        user = User(username, password, email, auth_token)
        db.session.add(user)
    if user.apps is None:
        application = Application("com.package")
        userApp = UserApp(user.id, application.app_key)

        build = Build(application.app_key, "11", "1.1", "rn", "http://...")

        db.session.add(application)
        db.session.add(userApp)

    track = Track('test1', time.time())
    db.session.add(track)

    db.session.commit()


