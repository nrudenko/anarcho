import datetime

from sqlalchemy import Table, Column, Integer, String, DateTime


def users(metadata):
    """ Create users table."""

    return Table('users', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('email', String(50), unique=True, nullable=False),
                 Column('name', String(20)),
                 Column('pass_hash', String(100)),
                 Column('created_on', DateTime, default=datetime.datetime.now, nullable=False))
