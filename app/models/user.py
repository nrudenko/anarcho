import time

from app import db
from app.models.base import Base
from flask.ext.login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class User(Base, db.Model, UserMixin):
    __tablename__ = "users"

    id = Column('user_id', Integer, primary_key=True)
    username = Column('username', String(20), unique=True, index=True)
    password = Column('password', String(10))
    email = Column('email', String(50), unique=True, index=True)
    registered_on = Column('registered_on', Integer)
    auth_token = Column('auth_token', String(50), unique=True, index=True)

    apps = relationship("Application", secondary="users_apps", backref="users")

    __json_fields__ = ['username', 'auth_token']

    def __init__(self, username, password, email, auth_token):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = time.time()
        self.auth_token = auth_token

    def __repr__(self):
        return '<User %r>' % (self.username)


class UserApp(Base, db.Model):
    __tablename__ = "users_apps"

    id = Column('_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.user_id'))
    app_key = Column('app_key', String, ForeignKey('apps.app_key'))

    def __init__(self, user_id, app_key):
        self.user_id = user_id
        self.app_key = app_key