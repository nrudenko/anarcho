from app.build_helper import save_build
import os
from app import app, db
from app.models.application import Application
from app.models.build import Build
from app.models.user import UserApp
from flask import request, jsonify
from flask.ext.cors import cross_origin
from flask.ext.login import login_required, current_user
from werkzeug.utils import secure_filename


@app.route('/api/apps/add', methods=['POST'])
@cross_origin(headers=['x-auth-token', 'Content-Type'])
@login_required
def app_create():
    name = request.json['name']
    print name
    new_app = Application(name)

    user_app = UserApp(current_user.id, new_app.app_key)
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
    return "{}"


@app.route('/api/apps/<app_key>/builds')
@cross_origin(headers=['x-auth-token'])
@login_required
def builds_list(app_key):
    result = Build.query.filter_by(app_key=app_key).all()
    return jsonify(list=[i.to_dict() for i in result])


@app.route('/api/builds')
@login_required
def builds():
    result = Build.query
    return jsonify([i.to_dict() for i in result.all()])


@app.route('/api/apps/<app_key>/upload', methods=['POST'])
@cross_origin(headers=['x-auth-token'])
@login_required
def upload(app_key):
    apk_file = request.files['file']
    if apk_file:
        filename = secure_filename(apk_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print apk_file
        apk_file.save(file_path)

        build = save_build(file_path, app_key)
        return build.to_json()
    return None
