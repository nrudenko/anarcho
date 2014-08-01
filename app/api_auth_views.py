from app import app, db
from app.auth import unauthorized
from app.models.user import User
from flask import request, g
from flask.ext.cors import cross_origin
from flask.ext.login import login_required


@app.route('/api/register', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def register():
    email = request.json['email']
    username = request.json['username']
    password = request.json['password']
    new_user = User(username, password, email)
    db.session.add(new_user)
    db.session.commit()
    return new_user.to_json()


@app.route('/api/login', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def login():
    username = request.json['username']
    password = request.json['password']
    registered_user = User.query.filter_by(username=username).first()
    if registered_user is not None and registered_user.verify_password(password):
        return registered_user.to_json()
    return unauthorized()


@app.route('/api/user', methods=['GET'])
@cross_origin(headers=['x-auth-token'])
@login_required
def user():
    return g.user.to_json()