#!flask/bin/python
import os

os.environ['DATABASE_URL'] = 'sqlite:///anarcho.db'

from app import app

app.run(debug=True)