#!/bin/bash

curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.9.tar.gz
tar xvfz virtualenv-1.9.tar.gz
virtualenv-1.9/virtualenv.py flask
rm virtualenv-1.9.tar.gz

source flask/bin/activate
pip install -r requirements.txt
python init_db.py local
python run.py