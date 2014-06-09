from datetime import datetime
from app import db
from sqlalchemy import Column, Integer, String, DateTime
from base import Base


class Application(Base, db.Model):
    __tablename__ = "apps"
    id = Column('app_id', Integer, primary_key=True)
    app_package = Column('app_package', String, unique=True)
    app_key = Column('app_key', String, unique=True)
    app_icon = Column('app_icon', String)
    created_on = Column('created_on', DateTime)

    def __init__(self, app_package, app_key):
        self.app_package = app_package
        self.app_key = app_key
        self.created_on = datetime.utcnow()

    def __repr__(self):
        return '<Application %r>' % (self.app_package)
