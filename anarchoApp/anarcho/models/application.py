import uuid

import time
from anarcho import db
from sqlalchemy import Column, Integer, String


class Application(db.Model):
    __tablename__ = "apps"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    package = Column('package', String)
    app_key = Column('app_key', String, unique=True)
    icon_url = Column('icon_url', String)
    created_on = Column('created_on', Integer)

    def __init__(self, name):
        self.name = name
        self.app_key = uuid.uuid1().__str__()
        self.created_on = time.time()

    def __repr__(self):
        return '<Application %r>' % self.name
