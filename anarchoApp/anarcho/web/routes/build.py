import datetime

from sqlalchemy import desc

from anarcho import app, db, storage_worker
from anarcho.old_access_manager import login_required, app_permissions
from anarcho.models.application import Application, ANDR, IOS
from anarcho.models.build import Build
from anarcho.serializer import serialize, BuildSerializer
from flask import request, redirect, Response, make_response, send_file, jsonify
from flask.templating import render_template


@app.route('/api/apps/<app_key>/builds', methods=['DELETE'])
@login_required
@app_permissions(permissions=["w"])
def delete_builds_list(app_key):
    ids = request.json['ids']
    builds = Build.query.filter(Build.app_key == app_key, Build.id.in_(ids)).all()
    for b in builds:
        db.session.delete(b)
        storage_worker.remove_build(b)
    db.session.commit()
    return Response(status=200)


@app.route('/api/apps/<app_key>/builds', methods=['GET'])
@login_required
def builds_list(app_key):
    builds = Build.query.filter_by(app_key=app_key).order_by(desc(Build.created_on)).all()
    return serialize(builds)


@app.route('/api/apps/<app_key>/<int:build_id>', methods=['GET'])
@login_required
def get_build(app_key, build_id):
    build = Build.query.filter_by(app_key=app_key, id=build_id).first()
    if build:
        fields = BuildSerializer(build).to_dict()
        fields.update({'build_url': storage_worker.get_build_link(build)})
        if build.app.app_type == IOS:
            install_url = 'itms-services://?action=download-manifest&' \
                          'url={host}/api/apps/{app_key}/{build_id}/plist' \
                .format(host=app.config['PUBLIC_HOST_SECURE'],
                        app_key=app_key,
                        build_id=build_id)
            fields.update({'install_url': install_url})
        return jsonify(fields)
    return make_response('{"error":"build_not_found"}', 404)


@app.route('/api/apps/<app_key>/<int:build_id>/notes', methods=['POST'])
@login_required
@app_permissions(permissions=["w"])
def update_build_notes(app_key, build_id):
    build = Build.query.filter_by(app_key=app_key, id=build_id).first()
    if build:
        build.release_notes = request.json['release_notes']
        db.session.commit()
        return serialize(build)
    return make_response('{"error":"build_not_found"}', 404)


@app.route('/api/apps/<app_key>/<int:build_id>/file', methods=['GET'])
def get_build_file(app_key, build_id):
    application = Application.query.filter_by(app_key=app_key).first()
    if not application:
        return make_response('{"error":"app_not_found"}', 404)
    build = Build.query.filter_by(app_key=app_key, id=build_id).first()
    if not build:
        return make_response('{"error":"build_not_found"}', 404)
    try:
        upload_date = datetime.datetime.fromtimestamp(build.created_on).strftime('%Y-%m-%d_%H-%M-%S')
        mime_type = None
        ext = None
        if application.app_type == ANDR:
            mime_type = 'application/vnd.android.package-archive'
            ext = 'apk'
        elif application.app_type == IOS:
            mime_type = 'application/octet-stream'
            ext = 'ipa'

        name = '{proj}_{date}.{ext}'.format(proj=application.name, date=upload_date, ext=ext)
        return send_file(storage_worker.get(build),
                         mimetype=mime_type,
                         as_attachment=True,
                         attachment_filename=name)
    except IOError:
        return make_response('{"error":"file_error"}', 400)


@app.route('/api/apps/<app_key>/<int:build_id>/plist', methods=['GET'])
def get_build_plist(app_key, build_id):
    application = Application.query.filter_by(app_key=app_key).first()
    if not application:
        return make_response('{"error":"app_not_found"}', 404)

    build = Build.query.filter_by(app_key=app_key, id=build_id).first()
    if not build:
        return make_response('{"error":"build_not_found"}', 404)
    build_url = storage_worker.get_build_link(build)
    return render_template('app.plist', bundle_id=application.package, build_url=build_url)


@app.route('/api/apps/<app_key>/<int:build_id>/install', methods=['GET'])
def redirect_to_instalation(app_key, build_id):
    application = Application.query.filter_by(app_key=app_key).first()
    if not application:
        return make_response('{"error":"app_not_found"}', 404)

    build = Build.query.filter_by(app_key=app_key, id=build_id).first()
    if not build:
        return make_response('{"error":"build_not_found"}', 404)
    build_url = storage_worker.get_build_link(build)
    return redirect(build_url)
