# from sqlite3 import dbapi2 as sqlite3
import sqlite3
from app import app
from flask import _app_ctx_stack, g


# def get_db():
#     """Opens a new database connection if there is none yet for the
#     current application context.
#     """
#     top = _app_ctx_stack.top
#     if not hasattr(top, 'sqlite_db'):
#         top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
#         top.sqlite_db.row_factory = sqlite3.Row
#     return top.sqlite_db

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db


@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


# @app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv