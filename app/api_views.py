from app import app, db
from app.models.application import Application
from app.models.build import Build
from app.models.user import User, UserApp
from flask import request, jsonify
from flask.ext.login import login_required, current_user


@app.route('/api/auth', methods=['POST'])
def auth():
    data = request.get_json()
    if data is not None:
        print data
        user = User.query.filter_by(username=data["username"], password=data["password"]).first()
    else:
        username = request.values.get('username')
        password = request.values.get('password')
        user = User.query.filter_by(username=username, password=password).first()
    if user:
        return '{"api_key":"' + user.api_key + '"}'
    return '{"error":"unauthorized"}'


@app.route('/api/apps', methods=['POST', 'GET'])
@login_required
def apps():
    if request.method == 'POST':
        package = request.values.get('package')
        new_app = Application(package)

        user_app = UserApp(current_user.id, new_app.app_key)
        db.session.add(new_app)
        db.session.add(user_app)
        db.session.commit()
        return '{"app_key":"' + new_app.app_key + '"}'
    return jsonify(data=[i.to_dict() for i in current_user.apps])


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
    print result
    return jsonify(data=[i.to_dict() for i in result])


@app.route('/api/builds')
@login_required
def builds():
    result = Build.query
    return jsonify([i.to_dict() for i in result.all()])

