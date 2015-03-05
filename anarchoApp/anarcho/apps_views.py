import datetime
from sqlalchemy import desc

from anarcho.models.token import Token
from anarcho.models.user import User
from flask.json import jsonify
import os
from anarcho import storage_worker, app, db
from anarcho.serializer import serialize
from anarcho.build_helper import parse_apk
from anarcho.access_manager import app_permissions, login_required
from flask.helpers import send_file
from anarcho.models.application import Application
from anarcho.models.build import Build
from anarcho.models.user_app import UserApp
from flask import request, Response, make_response, g
from flask.ext.cors import cross_origin
from werkzeug.utils import secure_filename
from storage_workers import LocalStorageWorker


@app.route('/api/apps', methods=['GET'])
@cross_origin(headers=['x-auth-token', 'Content-Type'])
@login_required
def apps_list():
    user_apps = UserApp.query.filter_by(user_id=g.user.id).all()
    return serialize(user_apps)


@app.route('/api/apps', methods=['POST', 'GET'])
@cross_origin(headers=['x-auth-token', 'Content-Type'])
@login_required
def app_create():
    name = request.json['name']
    new_app = Application(name)

    user_app = UserApp(g.user.id, new_app.app_key, "w")
    db.session.add(new_app)
    db.session.add(user_app)
    db.session.commit()

    api_user = User()
    db.session.add(api_user)
    db.session.commit()

    api_user_token = Token(api_user)
    api_user_app = UserApp(api_user.id, new_app.app_key, "u")
    db.session.add(api_user_app)
    db.session.add(api_user_token)
    db.session.commit()
    return serialize(user_app)


@app.route('/api/apps/<app_key>', methods=['DELETE'])
@cross_origin(headers=['x-auth-token', 'Content-Type'], methods=['DELETE'])
@login_required
@app_permissions(permissions=["w"])
def remove_application(app_key):
    application = Application.query.filter_by(app_key=app_key).first()
    if application:
        db.session.delete(application)
    db.session.commit()
    return Response(status=200)


@app.route('/api/apps/<app_key>', methods=['GET'])
@cross_origin(headers=['x-auth-token'])
@login_required
def app_info(app_key):
    application = UserApp.query.filter_by(app_key=app_key, user_id=g.user.id).first()
    if application:
        return serialize(application)
    return make_response('{"error":"app_not_found"}', 404)


@app.route('/api/apps/<app_key>', methods=['POST'])
@cross_origin(headers=['x-auth-token'])
@login_required
@app_permissions(permissions=['w', 'u'])
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
        application = Application.query.filter_by(app_key=app_key).first()
        package = result["package"]
        if application and application.package:
            if application.package != package:
                return make_response('{"error":"wrong_package"}', 406)
        elif application:
            application.package = package

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
    builds = Build.query.filter_by(app_key=app_key).order_by(desc(Build.created_on)).all()
    return serialize(builds)


@app.route('/api/apps/<app_key>/<int:build_id>', methods=['GET'])
@cross_origin(headers=['x-auth-token'])
@login_required
def get_build(app_key, build_id):
    build = Build.query.filter_by(app_key=app_key, id=build_id).first()
    if build:
        return serialize(build)
    return make_response('{"error":"build_not_found"}', 404)


@app.route('/api/apps/<app_key>/<int:build_id>/notes', methods=['POST'])
@cross_origin(headers=['x-auth-token', 'Content-Type'])
@login_required
@app_permissions(permissions=["w"])
def update_notes(app_key, build_id):
    build = Build.query.filter_by(app_key=app_key, id=build_id).first()
    if build:
        build.release_notes = request.json['release_notes']
        db.session.commit()
        return serialize(build)
    return make_response('{"error":"build_not_found"}', 404)


@app.route('/api/apps/<app_key>/<int:build_id>/file', methods=['GET'])
def get_build_file(app_key, build_id):
    build = Build.query.filter_by(app_key=app_key, id=build_id).first()
    if build is None:
        return make_response('{"error":"build_not_found"}', 404)
    try:
        application = Application.query.filter_by(app_key=build.app_key).first()
        upload_date = datetime.datetime.fromtimestamp(build.created_on).strftime('%Y-%m-%d_%H-%M-%S')
        name = '{proj}_{date}.apk'.format(proj=application.name, date=upload_date)
        return send_file(storage_worker.get(build),
                         mimetype='application/vnd.android.package-archive',
                         as_attachment=True,
                         attachment_filename=name)
    except IOError:
        return make_response('{"error":"build_not_found"}', 404)


@app.route('/api/icon/<app_key>', methods=['GET'])
def get_icon(app_key=None):
    if isinstance(storage_worker, LocalStorageWorker):
        icon_path = storage_worker.get_icon_path(app_key)
        if os.path.exists(icon_path):
            return send_file(icon_path)
    return Response(status=404)


@app.route('/api/apps/<app_key>/plugin', methods=['GET'])
@cross_origin(headers=['x-auth-token', 'Content-Type'])
@login_required
@app_permissions(permissions=['w', 'r'])
def get_plugin_config(app_key):
    user_app = UserApp.query.filter_by(app_key=app_key, permission='u').first()
    if user_app is None:
        return make_response('{"error":"app_not_found"}', 404)
    user = user_app.user
    response = {
        'uploadUrl': app.config['PUBLIC_HOST'] + '/api/apps/' + app_key,
        'apiToken': user.token.auth_token
    }
    return jsonify(response)
