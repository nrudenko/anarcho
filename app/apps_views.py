from app import storage_worker, app, db
from app.build_helper import parse_apk
from app.permission_manager import app_permissions
from flask.helpers import send_file
import os
from app.models.application import Application
from app.models.build import Build
from app.models.user import UserApp
from flask import request, jsonify, Response, make_response
from flask.ext.cors import cross_origin
from flask.ext.login import login_required, current_user
from werkzeug.utils import secure_filename
from storage_workers import LocalStorageWorker


@app.route('/api/apps/add', methods=['POST'])
@cross_origin(headers=['x-auth-token', 'Content-Type'])
@login_required
def app_create():
    name = request.json['name']
    new_app = Application(name)

    user_app = UserApp(current_user.id, new_app.app_key, "w")
    db.session.add(new_app)
    db.session.add(user_app)
    db.session.commit()
    return new_app.to_json()


@app.route('/api/apps/list', methods=['GET'])
@cross_origin(headers=['x-auth-token'])
@login_required
def apps_list():
    return jsonify(list=[i.to_dict() for i in current_user.apps])


@app.route('/api/apps/<app_key>')
@cross_origin(headers=['x-auth-token'])
@login_required
def app_info(app_key):
    application = Application.query.filter_by(app_key=app_key).first()
    if application:
        return application.to_json()
    return make_response('{"error":"app_not_found"}', 404)


@app.route('/api/apps/<app_key>/builds', methods=['DELETE'])
@cross_origin(headers=['x-auth-token', 'Content-Type'], methods=['DELETE'])
@login_required
@app_permissions(permissions=["w"])
def remove_build(app_key):
    ids = request.json['ids']
    builds = Build.query.filter(Build.app_key == app_key, Build.id.in_(ids)).all()
    for b in builds:
        db.session.delete(b)
        storage_worker.remove(b)
    db.session.commit()
    return Response(status=200)


@app.route('/api/apps/<app_key>/builds', methods=['GET'])
@cross_origin(headers=['x-auth-token'])
@login_required
def builds_list(app_key):
    result = Build.query.filter_by(app_key=app_key).all()
    return jsonify(list=[i.to_dict() for i in result])


@app.route('/api/apps/<app_key>/upload', methods=['POST'])
@cross_origin(headers=['x-auth-token'])
@login_required
def upload(app_key):
    apk_file = request.files['file']
    if apk_file:
        apk_filename = secure_filename(apk_file.filename)
        apk_file_path = os.path.join(app.config["TMP_DIR"], apk_filename)
        apk_file.save(apk_file_path)

        result = parse_apk(apk_file_path, app_key)

        build = result["build"]
        icon_path = result["icon_path"]

        db.session.add(build)
        db.session.commit()

        storage_worker.put(build, apk_file_path, icon_path)

        application = Application.query.filter_by(app_key=app_key).first()
        application.icon_url = storage_worker.get_icon_link(app_key)
        db.session.commit()
        return build.to_json()
    return make_response('{"error":"upload_error"}', 400)


@app.route('/api/apps/<app_key>/<int:build_id>', methods=['GET'])
def get_build(app_key, build_id):
    build = Build.query.filter_by(app_key=app_key, id=build_id).first()
    if build is None:
        return make_response('{"error":"build_not_found"}', 404)
    try:
        return storage_worker.get(build)
    except IOError:
        return make_response('{"error":"build_not_found"}', 404)


@app.route('/api/icon/<app_key>', methods=['GET'])
def get_icon(app_key):
    if isinstance(storage_worker, LocalStorageWorker):
        icon_path = storage_worker.get_icon_path(app_key)
        if os.path.exists(icon_path):
            return send_file(icon_path)
    return Response(status=404)