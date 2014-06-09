from datetime import datetime
from app import db

from app.models.base import Base
from sqlalchemy import Column, Integer, String, DateTime


class User(Base, db.Model):
    __tablename__ = "users"

    id = Column('user_id', Integer, primary_key=True)
    username = Column('username', String(20), unique=True, index=True)
    password = Column('password', String(10))
    email = Column('email', String(50), unique=True, index=True)
    registered_on = Column('registered_on', DateTime)
    api_key = Column('api_key', String(50), unique=True, index=True)

    def __init__(self, username, password, email, api_key):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
        self.api_key = api_key

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


class UserApp(Base, db.Model):
    __tablename__ = "users_apps"

    id = Column('_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer)
    app_key = Column('app_key', String)

    def __init__(self, user_id, app_key):
        self.user_id = user_id
        self.app_key = app_key