from app import app, db
from app.models.user import UserApp, User
from app.permission_manager import app_permissions
from flask import request, jsonify, make_response
from flask.ext.cors import cross_origin

from flask.ext.login import login_required


@app.route('/api/team/user', methods=['PATCH'])
@cross_origin(headers=['x-auth-token', 'Content-Type'], methods=['PATCH'])
@login_required
@app_permissions(permissions=["w"])
def update_user():
    app_key = request.json['app_key']
    email = request.json['email']
    permission = request.json['permission']
    user_app = UserApp.query.filter_by(app_key=app_key, email=email).first()
    if user_app is None:
        return make_response('{"error":"user_app_not_found}', 404)
    user_app.permission = permission
    db.session.commit()
    print user_app.to_json()
    return user_app.to_json()


@app.route('/api/team/user', methods=['POST'])
@cross_origin(headers=['x-auth-token', 'Content-Type'])
@login_required
@app_permissions(permissions=["w"])
def add_user():
    app_key = request.json['app_key']
    email = request.json['email']
    permission = request.json['permission']

    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(email)
    user_app = UserApp(email, app_key, permission)
    user_app.user = user
    db.session.add(user_app)
    db.session.commit()
    return user_app.to_json()


@app.route('/api/team/<app_key>/list/', methods=['GET'])
@cross_origin(headers=['x-auth-token', 'Content-Type'])
@login_required
@app_permissions(permissions=["w"])
def users_list(app_key):
    user_apps = UserApp.query.filter_by(app_key=app_key).all()

    return jsonify(list=[i.to_dict() for i in user_apps])


@app.route('/api/team/revoke', methods=['POST'])
@cross_origin(headers=['x-auth-token', 'Content-Type'])
@login_required
@app_permissions(permissions=["w"])
def revoke_team_membership():
    app_key = request.json['app_key']
    email = request.json['email']
    user_app = UserApp.query.filter_by(app_key=app_key, email=email).first()
    db.session.delete(user_app)
    db.session.commit()
    return user_app.to_json()