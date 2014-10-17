import time

from app import db
from app.models.base import Base
from flask.ext.login import UserMixin, make_secure_token
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base, db.Model, UserMixin):
    __tablename__ = "users"

    id = Column('id', Integer, primary_key=True)
    username = Column('username', String(20))
    pass_hash = Column('pass_hash', String)
    email = Column('email', String(50), unique=True)
    registered_on = Column('registered_on', Integer)
    auth_token = Column('auth_token', String(50), )
    apps = relationship("Application", secondary="users_apps", backref="users")

    __json_fields__ = ['id', 'username']

    def __init__(self, email, username=None, password=None):
        self.email = email
        self.username = username
        if username is not None and password is not None:
            self.username = username
            self.hash_password(password)
            self.registered_on = time.time()
            self.update_auth_token()

    def update_auth_token(self):
        self.auth_token = make_secure_token(self.email, self.username)

    def hash_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_hash, password)

    def __repr__(self):
        return self.to_dict()


class UserApp(Base, db.Model):
    __tablename__ = "users_apps"

    id = Column('_id', Integer, primary_key=True)
    email = Column('email', String, ForeignKey('users.email'))
    app_key = Column('app_key', String, ForeignKey('apps.app_key'))
    permission = Column('permission', String)  # r/w/

    user = relationship("User", backref='users_apps')

    __json_fields__ = ['app_key', 'permission', 'username', 'email']

    def __init__(self, email, app_key, permission):
        self.email = email
        self.app_key = app_key
        self.permission = permission

    def username(self):
        return self.user.username