import time
import subprocess
from app.db_utils import get_db, query_db
import os
from app import app
from flask import request, session, redirect, url_for, render_template, flash, g
import re
from werkzeug.security import generate_password_hash, check_password_hash


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?',
                          [session['user_id']], one=True)


def get_user_id(username):
    """Convenience method to look up the id for a username."""
    rv = query_db('select user_id from user where username = ?',
                  [username], one=True)
    return rv[1] if rv else None


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user:
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        user = query_db('''select * from user where username = ?''', [request.form['username']], one=True)
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['pw_hash'], request.form['password']):
            error = 'Invalid password'
        else:
            session['user_id'] = user['user_id']
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    if g.user:
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                        '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            db = get_db()
            db.execute('''insert into user (
              username, email, pw_hash) values (?, ?, ?)''',
                       [request.form['username'], request.form['email'],
                        generate_password_hash(request.form['password'])])
            db.commit()
            return redirect(url_for('login'))
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/upload', methods=['POST'])
def upload():
    folder = os.path.abspath(app.config['UPLOAD_FOLDER'])

    file_name = str(int(time.time() * 1000))
    file_path = os.path.join(folder, file_name)
    fo = open(file_path, "wb")
    fo.write(request.data)
    fo.close()
    parse_apk(file_name, file_path)
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
    db = get_db()
    db.execute('''insert into build (
              app_id, pub_date, version,release_notes ,url) values (?, ?, ?,?,?)''',
               [file_name, file_name, version_code, package + ' ' + version_name, 'http://' + file_name])
    db.commit()


@app.route('/guide')
def guide():
    return render_template('guide.html')