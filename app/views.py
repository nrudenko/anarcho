import time
import subprocess
from app.database import db_session
from flask.ext.login import login_user, login_required, logout_user
import os
from app import app, login_manager
from app.models.user import User
from flask import request, session, redirect, url_for, render_template, flash, g
import re


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        print(session['user_id'])
        g.user = load_user(session['user_id'])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'], request.form['password'], request.form['email'])
    db_session.add(user)
    db_session.commit()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        print g.user
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        return redirect(url_for('login'))
    login_user(registered_user)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/guide')
@login_required
def guide():
    return render_template('guide.html')


@app.route('/upload', methods=['POST'])
@login_required
def upload():
    folder = os.path.abspath(app.config['UPLOAD_FOLDER'])

    file_name = str(int(time.time() * 1000))
    file_path = os.path.join(folder, file_name)
    fo = open(file_path, "wb")
    fo.write(request.data)
    fo.close()
    parse_apk(file_name, file_path)
    return redirect(url_for('index'))


@app.route('/add_app', methods=['POST'])
@login_required
def add_application():
    return redirect(url_for('index'))


def parse_apk(file_name, apk_path):
    args = ("utils/aapt", "d", "badging", apk_path)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    pattern = re.compile(
        r'package:\sname=\'(?P<name>.*?)\'\sversionCode=\'(?P<versionCode>.*?)\'\sversionName=\'(?P<versionName>.*?)\'',
        re.VERBOSE)
    match = pattern.match(output)
    package = match.group("name")
    version_code = match.group("versionCode")
    version_name = match.group("versionName")

    # db = get_db()
    # db.execute('''insert into build (
    #           app_id, pub_date, version,release_notes ,url) values (?, ?, ?,?,?)''',
    #            [file_name, file_name, version_code, package + ' ' + version_name, 'http://' + file_name])
    # db.commit()