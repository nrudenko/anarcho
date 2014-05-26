from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
# from app.database import Base
from app import db

class Application(db.Model):
    __tablename__ = "apps"
    id = Column('app_id', Integer, primary_key=True)
    app_package = Column('app_package', String, unique=True)
    app_key = Column('app_key', String, unique=True)
    created_on = Column('created_on', DateTime)

    def __init__(self, app_package, app_key):
        self.app_package = app_package
        self.app_key = app_key
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return '<Application %r>' % (self.app_package)
