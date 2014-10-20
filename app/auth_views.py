from app import app, db
from app.api_models import serialize, SessionSerializer
from app.auth import unauthorized
from app.models.user import User
from flask import request, g
from flask.ext.cors import cross_origin
from flask.ext.login import login_required
from sqlalchemy import or_


@app.route('/api/register', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def register():
    email = request.json['email']
    name = request.json['username']
    password = request.json['password']
    new_user = User(email, name, password)
    db.session.add(new_user)
    db.session.commit()
    return serialize(new_user, SessionSerializer)


@app.route('/api/login', methods=['POST'])
@cross_origin(headers=['Content-Type', 'x-auth-token'])
def login():
    username = request.json['username']
    password = request.json['password']
    registered_user = User.query.filter(or_(User.name == username, User.email == username)).first()
    if registered_user is not None and registered_user.verify_password(password):
        return serialize(registered_user, SessionSerializer)
    return unauthorized()


@app.route('/api/user', methods=['GET'])
@cross_origin(headers=['x-auth-token'])
@login_required
def user():
    return serialize(g.user)