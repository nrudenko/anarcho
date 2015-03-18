from anarcho.models.token import Token
from anarcho.models.user import User
from flask.json import jsonify
import os
from anarcho import storage_worker, app, db
from anarcho.serializer import serialize
from anarcho.access_manager import app_permissions, login_required
from flask.helpers import send_file
from anarcho.models.application import Application
from anarcho.models.user_app import UserApp
from flask import request, Response, make_response, g
from anarcho.storage_workers import LocalStorageWorker


@app.route('/api/apps', methods=['GET'])
@login_required
def apps_list():
    user_apps = UserApp.query.filter_by(user_id=g.user.id).all()
    return serialize(user_apps)


@app.route('/api/apps', methods=['POST'])
@login_required
def app_create():
    name = request.json['name']
    new_app = Application(name)

    user_app = UserApp(g.user.id, new_app.app_key, "w")
    db.session.add(new_app)
    db.session.add(user_app)
    db.session.commit()

    api_user = User(name='guest_{0}'.format(name))
    db.session.add(api_user)
    db.session.commit()

    api_user_token = Token(api_user)
    api_user_app = UserApp(api_user.id, new_app.app_key, "u")
    db.session.add(api_user_app)
    db.session.add(api_user_token)
    db.session.commit()
    return serialize(user_app)


@app.route('/api/apps/<app_key>', methods=['DELETE'])
@login_required
@app_permissions(permissions=["w"])
def remove_application(app_key):
    application = Application.query.filter_by(app_key=app_key).first()
    if application:
        db.session.delete(application)
    db.session.commit()
    return Response(status=200)


@app.route('/api/apps/<app_key>', methods=['GET'])
@login_required
def app_info(app_key):
    application = UserApp.query.filter_by(app_key=app_key, user_id=g.user.id).first()
    if application:
        application.icon_url = storage_worker.get_icon_link(app_key)
        return serialize(application)
    return make_response('{"error":"app_not_found"}', 404)


@app.route('/api/icon/<app_key>', methods=['GET'])
def get_icon(app_key=None):
    if isinstance(storage_worker, LocalStorageWorker):
        icon_path = storage_worker.get_icon_path(app_key)
        if os.path.exists(icon_path):
            return send_file(icon_path)
    return Response(status=404)


@app.route('/api/apps/<app_key>/plugin', methods=['GET'])
@login_required
@app_permissions(permissions=['w', 'r'])
def get_plugin_config(app_key):
    user_app = UserApp.query.filter_by(app_key=app_key, permission='u').first()
    if user_app is None:
        return make_response('{"error":"app_not_found"}', 404)
    user = user_app.user
    response = {
        'host': app.config['PUBLIC_HOST'],
        'app_key': app_key,
        'api_token': user.token.auth_token
    }
    return jsonify(response)
