from anarcho import app, db
from anarcho.access_manager import login_required
from anarcho.models.token import Token
from anarcho.serializer import serialize
from anarcho.models.user import User
from flask import request, g, Response
from flask.ext.cors import cross_origin


@app.route('/api/register', methods=['POST'])
@cross_origin(headers=['Content-Type', 'x-auth-token'])
def register():
    email = request.json['email']
    name = request.json['name']
    password = request.json['password']
    u = User.query.filter(User.email == email).first()
    if u is None:
        new_user = User(email, name, password)
        db.session.add(new_user)
        db.session.commit()

        token = Token(new_user)
        db.session.add(token)
        db.session.commit()
        return serialize(token)

    return Response('{"error":"user_already_registered"}', 409)


@app.route('/api/login', methods=['POST'])
@cross_origin(headers=['Content-Type', 'x-auth-token'])
def login():
    email = request.json['email']
    password = request.json['password']
    u = User.query.filter(User.email == email).first()
    if u is not None:
        if u.verify_password(password):
            return serialize(u.token)

    return Response('{"error":"wrong_credentials"}', 403)


@app.route('/api/user', methods=['GET'])
@cross_origin(headers=['x-auth-token'])
@login_required
def user():
    return serialize(g.user)