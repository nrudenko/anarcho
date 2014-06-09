#!flask/bin/python
import os
os.environ['DATABASE_URL'] = 'sqlite:///anarcho.db'

from app import app
import init_db

app.run(debug=True)
