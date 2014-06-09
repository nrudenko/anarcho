from datetime import datetime
from app import db
from sqlalchemy import Column, Integer, String, DateTime
from base import Base


class Build(db.Model, Base):
    __tablename__ = "builds"
    id = Column('build_id', Integer, primary_key=True)
    app_id = Column('app_id', String)
    version_code = Column('version_code', Integer)
    version_name = Column('version_name', String)
    release_notes = Column('release_notes', String)
    url = Column('url', String)
    created_on = Column('created_on', DateTime)

    __json_fields__ = ["app_id",
                       'version_code',
                       'version_name',
                       'release_notes',
                       'url',
                       'created_on']

    def __init__(self, app_id, version_code, version_name, release_notes, url):
        self.app_id = app_id
        self.version_code = version_code
        self.version_name = version_name
        self.release_notes = release_notes
        self.url = url
        self.created_on = datetime.utcnow()

    def __repr__(self):
        return '<Build %r>' % (self.app_id)

