from app import app, db
from app.models.application import Application
from app.models.build import Build
from app.models.user import UserApp
from flask import request, jsonify
from flask.ext.cors import cross_origin
from flask.ext.login import login_required, current_user


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
@login_required
def app_info(app_key):
    application = Application.query.filter_by(app_key=app_key).first()
    if application:
        return application.to_json()
    return "{}"


@app.route('/api/apps/<app_key>/add_build')
@login_required
def app_add_build(app_key):
    return '{upload build for app:' + app_key + '}'


@app.route('/api/apps/<app_key>/builds')
@login_required
def builds_list(app_key):
    result = Build.query.filter_by(app_key=app_key).all()
    return jsonify(data=[i.to_dict() for i in result])


@app.route('/api/builds')
@login_required
def builds():
    result = Build.query
    return jsonify([i.to_dict() for i in result.all()])

