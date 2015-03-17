from anarcho import app, db, storage_worker
from anarcho.access_manager import login_required, app_permissions
from anarcho.apk_helper import parse_apk
from anarcho.ipa_helper import parse_ipa
from anarcho.models.application import Application, IOS, ANDR
from anarcho.serializer import serialize
from flask import request, make_response
import os
from werkzeug.utils import secure_filename


def get_app_type(filename):
    if "ipa" in filename:
        app_type = IOS
    elif "apk" in filename:
        app_type = ANDR
    else:
        raise TypeError('Unknown file type. Supported types: ipa, apk.')
    return app_type


@app.route('/api/apps/<app_key>', methods=['POST'])
@login_required
@app_permissions(permissions=['w', 'u'])
def upload(app_key):
    application = Application.query.filter_by(app_key=app_key).first()

    if not application:
        return make_response('{"error":"app_not_found"}', 406)
    else:
        build_file = request.files['file']
        if build_file:
            filename = secure_filename(build_file.filename)
            file_path = os.path.join(app.config["TMP_DIR"], filename)
            build_file.save(file_path)
        else:
            return make_response('{"error":"build_file_absent"}', 406)

        try:
            app_type = get_app_type(filename)
        except TypeError:
            return make_response('{"error":"wrong_file_extension"}', 406)

        if not application.app_type:
            application.app_type = app_type
        elif application.app_type != app_type:
            return make_response('{"error":"wrong_app_type"}', 406)

        try:
            if app_type == ANDR:
                result = parse_apk(file_path, app_key)
            elif app_type == IOS:
                result = parse_ipa(file_path, app_key)
        except Exception:
            return make_response('{"error":"invalid_file_format"}', 406)

        package = result["package"]
        icon_path = result["icon_path"]
        build = result["build"]

        if not application.package:
            application.package = package
        elif application.package != package:
            return make_response('{"error":"wrong_package"}', 406)

        if 'releaseNotes' in request.form:
            release_notes = request.form['releaseNotes']
        else:
            release_notes = 'empty notes'
        build.release_notes = release_notes

        db.session.add(build)
        db.session.commit()

        storage_worker.put(build, file_path, icon_path)

        return serialize(build)

    return make_response('{"error":"upload_error"}', 400)

