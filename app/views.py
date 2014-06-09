import time
from app.build_helper import save_build
from flask.ext.login import login_user, login_required, logout_user
import os
from app import app, login_manager, db, APKParser
from app.models.user import User
from flask import request, session, redirect, url_for, render_template, flash, g
import re



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
    save_build(file_path)
    return redirect(url_for('index'))


@app.route('/add_app', methods=['POST'])
@login_required
def add_application():
    return redirect(url_for('index'))