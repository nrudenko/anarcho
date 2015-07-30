import datetime

from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey


def apps(metadata):
    """ Create apps table."""
    return Table('apps', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('app_key', String(64), unique=True),
                 Column('package', String(256)),
                 Column('name', String(20)),
                 Column('app_type', String(4)),
                 Column('created_on', DateTime, default=datetime.datetime.now, nullable=False)
                 )


def user_app(metadata):
    """ Create user_app table."""
    return Table('user_app', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('user_id', Integer),
                 Column('app_key', String(64), ForeignKey('apps.app_key', ondelete='CASCADE'), nullable=False),
                 Column('permissions', String(16)),
                 Column('created_on', DateTime, default=datetime.datetime.now, nullable=False)
                 )
