from anarcho import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class UserApp(db.Model):
    __tablename__ = "users_apps"

    id = Column('_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    app_key = Column('app_key', String, ForeignKey('apps.app_key'))
    permission = Column('permission', String)  # r/w/u

    user = relationship("User", backref='users_apps')
    app = relationship("Application", backref='users_apps')

    def __init__(self, user_id, app_key, permission):
        self.user_id = user_id
        self.app_key = app_key
        self.permission = permission