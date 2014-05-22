import time
import os
from app import app
from flask import request, session, redirect, url_for, render_template, flash


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


@app.route('/upload', methods=['POST'])
def upload():
    folder = os.path.abspath(app.config['UPLOAD_FOLDER'])
    file_name = str(int(time.time() * 1000))
    file_path = os.path.join(folder, file_name)
    fo = open(file_path, "wb")
    fo.write(request.data)
    fo.close()
    return redirect(url_for('index'))