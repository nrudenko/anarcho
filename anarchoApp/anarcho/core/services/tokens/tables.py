import datetime

from sqlalchemy import Column, Integer, String, Table, DateTime


def tokens(metadata):
    return Table('tokens', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('auth_id', String(28), nullable=False),
                 Column('value', String(32), nullable=False),
                 Column('expires_on', DateTime),
                 Column('created_on', DateTime, default=datetime.datetime.now, nullable=False)
                 )
