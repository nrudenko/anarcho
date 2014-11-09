import os

from anarcho import storage_worker, app, db
from anarcho.serializer import serialize
from anarcho.build_helper import parse_apk
from anarcho.permission_manager import app_permissions
from flask.helpers import send_file
from anarcho.models.application import Application
from anarcho.models.build import Build
from anarcho.models.user_app import UserApp
from flask import request, Response, make_response
from flask.ext.cors import cross_origin
from flask.ext.login import login_required, current_user
from werkzeug.utils import secure_filename
from storage_workers import LocalStorageWorker


@app.route('/api/apps', methods=['POST', 'GET'])
@cross_origin(headers=['x-auth-token', 'Content-Type'])
@login_required
def app_create():
    if request.method == 'GET':
        user_apps = UserApp.query.filter_by(email=current_user.email).all()
        return serialize(user_apps)
    else:
        name = request.json['name']
        new_app = Application(name)

        user_app = UserApp(current_user.email, new_app.app_key, "w")
        db.session.add(new_app)
        db.session.add(user_app)
        db.session.commit()
        return serialize(user_app)


@app.route('/api/apps/<app_key>', methods=['GET'])
@cross_origin(headers=['x-auth-token'])
@login_required
@app_permissions(permissions=['r', 'w'])
def app_info(app_key):
    application = UserApp.query.filter_by(app_key=app_key, email=current_user.email).first()
    if application:
        return serialize(application)
    return make_response('{"error":"app_not_found"}', 404)


@app.route('/api/apps/<app_key>', methods=['POST'])
@cross_origin(headers=['x-auth-token'])
@login_required
@app_permissions(permissions=['w'])
def upload(app_key):
    release_notes = 'empty'
    if 'releaseNotes' in request.form:
        release_notes = request.form['releaseNotes']
    apk_file = request.files['file']
    if apk_file:
        apk_filename = secure_filename(apk_file.filename)
        apk_file_path = os.path.join(app.config["TMP_DIR"], apk_filename)
        apk_file.save(apk_file_path)

        result = parse_apk(apk_file_path, app_key)

        build = result["build"]
        icon_path = result["icon_path"]
        build.release_notes = release_notes
        db.session.add(build)
        db.session.commit()

        storage_worker.put(build, apk_file_path, icon_path)

        application = Application.query.filter_by(app_key=app_key).first()
        application.icon_url = storage_worker.get_icon_link(app_key)
        db.session.commit()
        return serialize(build)
    return make_response('{"error":"upload_error"}', 400)


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
    builds = Build.query.filter_by(app_key=app_key).all()
    return serialize(builds)


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
def get_icon(app_key=None):
    if isinstance(storage_worker, LocalStorageWorker):
        icon_path = storage_worker.get_icon_path(app_key)
        if os.path.exists(icon_path):
            return send_file(icon_path)
    return Response(status=404)