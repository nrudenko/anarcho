from app import app, db
from app.api_models import serialize, SessionSerializer
from app.models.user import User
from flask import request, g, Response
from flask.ext.cors import cross_origin
from flask.ext.login import login_required


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
        return serialize(new_user, SessionSerializer)
    else:
        return Response('{"error":"user_already_registered"}', 409)


@app.route('/api/login', methods=['POST'])
@cross_origin(headers=['Content-Type', 'x-auth-token'])
def login():
    email = request.json['email']
    password = request.json['password']
    registered_user = User.query.filter(User.email == email).first()
    if registered_user is not None:
        if registered_user.verify_password(password):
            return serialize(registered_user, SessionSerializer)
        else:
            return Response('{"error":"wrong_credentials"}', 403)
    return Response('{"error":"user_not_found"}', 404)


@app.route('/api/user', methods=['GET'])
@cross_origin(headers=['x-auth-token'])
@login_required
def user():
    return serialize(g.user)