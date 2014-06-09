import json
from app import app, db
from app.models.build import Build
from app.models.user import User
from flask import request, jsonify
from flask.ext.login import current_user, login_required


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if data is not None:
        print data
        user = User.query.filter_by(username=data["username"], password=data["password"]).first()
    else:
        username = request.values.get('username')
        password = request.values.get('password')
        user = User.query.filter_by(username=username, password=password).first()
    if user:
        return '{api_key:"' + user.api_key + '"}'
    return '{"error":"unauthorized"}'


@app.route('/api/app/')
@login_required
def api_app_list():
    return '{app list}'


@app.route('/api/app/new')
@login_required
def api_app_new():
    return '{"app created"}'


@app.route('/api/app/<id>/upload')
@login_required
def api_app_upload(id):
    return '{upload build for app:' + id + '}'


@app.route('/api/app/<id>')
@login_required
def api_app(id):
    return '{app info ' + id + '}'


@app.route('/api/app/<id>/builds')
@login_required
def api_build_list():
    return '{}'


@app.route('/api/builds')
@login_required
def api_builds():
    result = Build.query
    return jsonify(data=[i.to_dict() for i in result.all()])

