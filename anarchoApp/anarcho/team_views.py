import re
from anarcho import app, db
from anarcho.serializer import serialize, PermissionSerializer
from anarcho.models.user import User
from anarcho.models.user_app import UserApp
from anarcho.access_manager import app_permissions, login_required, is_permission_allowed
from flask import request, make_response, g
from flask.ext.cors import cross_origin


@app.route('/api/permission/<app_key>', methods=['GET'])
@cross_origin(headers=['x-auth-token'])
@login_required
@app_permissions(permissions=["w"])
def users_list(app_key=None):
    user_apps = UserApp.query.filter(UserApp.app_key == app_key, UserApp.permission != 'u').all()
    return serialize(user_apps, serializer=PermissionSerializer)


@app.route('/api/permission', methods=['POST', 'PATCH', 'DELETE'])
@cross_origin(headers=['x-auth-token', 'Content-Type'], methods=['POST', 'PATCH', 'DELETE'])
@login_required
@app_permissions(permissions=["w"])
def revoke_team_membership():
    if request.method == 'POST':
        result = add_user()
    if request.method == 'PATCH':
        result = update_permission(get_user_app())
    if request.method == 'DELETE':
        result = remove_permission(get_user_app())
    return result


def get_user_app():
    email = request.json['email']
    app_key = request.json['app_key']
    user = User.query.filter_by(email=email).first()
    if user:
        return UserApp.query.filter_by(app_key=app_key, user_id=user.id).first()


def remove_permission(user_app):
    email = request.json['email']
    if g.user.email == email:
        return make_response('{"error":"user_can_not_delete_himself"}', 403)
    elif user_app:
        result = serialize(user_app, PermissionSerializer)
        db.session.delete(user_app)
        db.session.commit()
        return result
    else:
        return make_response('{"error":"user_app_not_found}', 404)


def update_permission(user_app):
    email = request.json['email']
    permission = request.json['permission']
    if g.user.email == email:
        return make_response('{"error":"user_can_not_change_permission"}', 403)
    elif not is_permission_allowed(permission):
        result = make_response('{"error":"wrong_permission}', 400)
    elif user_app:
        user_app.permission = permission
        db.session.commit()
        result = serialize(user_app, PermissionSerializer)
    else:
        result = make_response('{"error":"user_app_not_found}', 404)
    return result


def add_user():
    app_key = request.json['app_key']
    email = request.json['email']
    permission = request.json['permission']
    valid_email_regex = re.match(r'\w[\w\.-]*@\w[\w\.-]+\.\w+', email)

    user = User.query.filter_by(email=email).first()
    application = None
    if user is not None:
        application = UserApp.query.filter_by(app_key=app_key, user_id=user.id).first()
    if application is not None:
        return make_response('{"error":"user_with_current_email_already_exist"}', 409)
    elif len(email) > 25:
        return make_response('{"error":"invalid_email_length"}', 403)
    elif valid_email_regex is None:
        return make_response('{"error":"invalid_email_format"}', 403)
    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(email)
        db.session.add(user)
        db.session.commit()
    user_app = UserApp(user.id, app_key, permission)
    user_app.user = user
    db.session.add(user_app)
    db.session.commit()
    return serialize(user_app, PermissionSerializer)