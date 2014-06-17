import uuid
import time

from app import db
from sqlalchemy import Column, Integer, String, LargeBinary
from base import Base


class Application(Base, db.Model):
    __tablename__ = "apps"
    id = Column('app_id', Integer, primary_key=True)
    app_package = Column('app_package', String, unique=True)
    app_key = Column('app_key', String, unique=True)
    app_icon = Column('app_icon', LargeBinary)
    created_on = Column('created_on', Integer)

    __json_fields__ = {"app_package", "app_key", "app_icon", "created_on"}

    def __init__(self, app_package):
        self.app_package = app_package
        self.app_key = uuid.uuid1().__str__()
        self.created_on = time.time()

    def __repr__(self):
        return '<Application %r>' % (self.app_key)
