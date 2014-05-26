#!/usr/bin/python
import os, subprocess

subprocess.call(['virtualenv-1.11.6/virtualenv.py', 'flask'])

subprocess.call([os.path.join('flask', 'bin', 'pip'), 'install', 'gunicorn'])
subprocess.call([os.path.join('flask', 'bin', 'pip'), 'install', 'flask'])
subprocess.call([os.path.join('flask', 'bin', 'pip'), 'install', 'flask-login'])

subprocess.call([os.path.join('flask', 'bin', 'pip'), 'install', 'sqlalchemy'])
subprocess.call([os.path.join('flask', 'bin', 'pip'), 'install', 'flask-sqlalchemy'])
subprocess.call([os.path.join('flask', 'bin', 'pip'), 'install', 'flask-psycopg2'])


# subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask-openid'])
#subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask-mail'])
# subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'sqlalchemy-migrate'])
# subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask-whooshalchemy'])
# subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask-wtf'])
# subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flask-babel'])
# subprocess.call([os.path.join('flask', bin, 'pip'), 'install', 'flup'])
