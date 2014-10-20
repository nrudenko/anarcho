import time

from app import db
from sqlalchemy import Column, Integer, String


class Track(db.Model):
    __tablename__ = "tracks"
    id = Column('track_id', Integer, primary_key=True)
    track_log = Column('track_log', String)
    track_key = Column('track_key', String)
    track_time = Column('track_time', Integer)
    created_on = Column('created_on', Integer)

    def __init__(self, track_log, track_time):
        self.track_log = track_log
        self.track_time = track_time
        self.created_on = time.time()