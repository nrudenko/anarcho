import time

from app.build_helper import save_build
from flask.ext.login import login_required
import os
from app import app
from flask import request, redirect, url_for, render_template


@app.route('/')
def index():
    return render_template('index.html')


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