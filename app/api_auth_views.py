from app import app, db
from app.auth import unauthorized
from app.models.user import User
from flask import request, g
from flask.ext.cors import cross_origin
from flask.ext.login import make_secure_token, login_required


@app.route('/api/register', methods=['POST'])
def register():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    api_key = make_secure_token(email, username, password)
    user = User(username, password, email, api_key)
    db.session.add(user)
    db.session.commit()
    return user.to_json()


@app.route('/api/login', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def login():
    username = request.json['username']
    password = request.json['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        return unauthorized()
    return registered_user.to_json()


@app.route('/api/user', methods=['GET'])
@cross_origin(headers=['x-auth-token'])
@login_required
def user():
    return g.user.to_json()