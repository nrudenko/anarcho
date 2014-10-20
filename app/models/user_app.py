from app import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class UserApp(db.Model):
    __tablename__ = "users_apps"

    id = Column('_id', Integer, primary_key=True)
    email = Column('email', String, ForeignKey('users.email'))
    app_key = Column('app_key', String, ForeignKey('apps.app_key'))
    permission = Column('permission', String)  # r/w/

    user = relationship("User", backref='users_apps')
    app = relationship("Application", backref='users_apps')

    def __init__(self, email, app_key, permission):
        self.email = email
        self.app_key = app_key
        self.permission = permission