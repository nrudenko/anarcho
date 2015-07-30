from flask import Blueprint, request
from objects.injections import inject, KwArg

from anarcho.core.core_catalog import Services
from anarcho.core.services.apps.exceptions import AppNotFound
from anarcho.extensions.api_login.manager import login_required
from anarcho.web.exceptions import AnarchoApiException
from anarcho.web.responses import AppsListResponse, json_response, AppResponse

apps_views = Blueprint('apps', __name__, url_prefix='/api')


@apps_views.route('/apps', methods=['GET'])
@login_required
@inject(KwArg('apps_service', Services.apps))
def list_apps(user, apps_service):
    """
    Return list of apps allowed for current user
    :param user:
    :type user: User
    :param apps_service:
    :type apps_service: anarcho.core.services.apps.service.Apps
    """
    apps = apps_service.get_user_apps(user.id)
    return json_response(AppsListResponse(apps))


@apps_views.route('/apps', methods=['PUT'])
@login_required
@inject(KwArg('_request', request))
@inject(KwArg('apps_service', Services.apps))
def new_user_app(user, _request, apps_service):
    """
    Create new app for current user
    :param user:
    :type user: User
    :param _request:
    :param apps_service:
    :type apps_service: anarcho.core.services.apps.service.Apps
    """
    json = _request.json
    name = json.get('name')
    app = apps_service.add_new_user_app(name, user.id)
    return json_response(AppResponse(app))


@apps_views.route('/apps/<app_key>', methods=['DELETE'])
@login_required
@inject(KwArg('apps_service', Services.apps))
# @app_permissions(permissions=["w"])
def delete_app(app_key, apps_service):
    """
    Delete app by app_key
    :param user:
    :type user: User
    :param app_key:
    :param apps_service:
    :type apps_service: anarcho.core.services.apps.service.Apps
    """
    apps_service.delete_app(app_key)


@apps_views.route('/apps/<app_key>', methods=['GET'])
@login_required
@inject(KwArg('apps_service', Services.apps))
def get_app(user, app_key, apps_service):
    """
    Get app
    :param user:
    :type user: User
    :param app_key:
    :param apps_service:
    :type apps_service: anarcho.core.services.apps.service.Apps
    """
    try:
        app = apps_service.get_user_app(user.id, app_key)
        return json_response(AppResponse(app))
    except AppNotFound as e:
        raise AnarchoApiException(e, 404)
    except Exception:
        # todo handle error
        raise AnarchoApiException('', 500)


@apps_views.route('/apps/<app_key>/icon', methods=['GET'])
def get_icon(user, app_key):
    # if isinstance(storage_worker, LocalStorageWorker):
    #     icon_path = storage_worker.get_icon_path(app_key)
    #     if os.path.exists(icon_path):
    #         return send_file(icon_path)
    # return Response(status=404)
    pass


@apps_views.route('/apps/<app_key>/plugin', methods=['GET'])
@login_required
# @app_permissions(permissions=['w', 'r'])
def get_plugin_config(user, app_key):
    # user_app = UserApp.query.filter_by(app_key=app_key, permission='u').first()
    # if user_app is None:
    #     return make_response('{"error":"app_not_found"}', 404)
    # user = user_app.user
    # response = {
    #     'host': app.config['PUBLIC_HOST'],
    #     'app_key': app_key,
    #     'api_token': user.token.auth_token
    # }
    # return jsonify(response)
    pass
