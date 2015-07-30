import os
import uuid
from os.path import expanduser

from flask import Flask, make_response
from flask.ext.cors import cross_origin

from objects.injections import inject, KwArg

from anarcho.core.core_catalog import Services
from anarcho.extensions.api_login.manager import ApiLoginManager
from anarcho.web.exceptions import AnarchoApiException
from anarcho.web.views.apps import apps_views
from anarcho.web.views.auth import auth_views
from anarcho.web.views.general import general
from anarcho.web.views.users import users_views

default_config_path = os.path.join(expanduser("~"), ".anarcho", "config.py")


@cross_origin(headers=['x-auth-token', 'Content-Type'],
              methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def cross_origin(response):
    """
    Apply CORS for all requests
    :param response:
    :return:
    """
    return response


def exception_handler(error):
    if isinstance(error, AnarchoApiException):
        return make_response('{"error":"' + error.message + '"}', error.status_code)
    else:
        print 'Raised not ApiException:', error


@inject(KwArg('users_service', Services.users))
@inject(KwArg('tokens_service', Services.tokens))
def load_user(token_value, tokens_service, users_service):
    """

    :param token_value:
    :param tokens_service:
    :type tokens_service: anarcho.core.services.tokens.service.Tokens
    :param users_service:
    :type users_service: anarcho.core.services.users.service.Users
    :return:
    """
    token = tokens_service.get_token_by_value(token_value)
    user = users_service.get_user_by_email(token.auth_id)
    return user


def init_app(app, config_path=default_config_path):
    """

    :param app:
    :type app: Flask
    """
    app.config.update({'SECRET_KEY': str(uuid.uuid4())})
    if os.path.exists(config_path):
        app.config.from_pyfile(config_path)
    else:
        raise ValueError("Configuration file {0} does not exist. "
                         "Use 'anarcho init' to initialize the file.".format(config_path))
    api_login_manager = ApiLoginManager(app)
    api_login_manager.load_user(load_user)

    app.after_request(cross_origin)
    app.register_error_handler(Exception, exception_handler)

    app.register_blueprint(general)
    app.register_blueprint(auth_views)
    app.register_blueprint(users_views)
    app.register_blueprint(apps_views)


def create_app():
    app = Flask(__name__)

    init_app(app)
    return app

    # def create_folders():
    #     tmp_dir = app.config["TMP_DIR"]
    #     if not os.path.exists(tmp_dir):
    #         os.makedirs(tmp_dir)
    #     logs_dir = app.config["LOGS_DIR"]
    #     if not os.path.exists(logs_dir):
    #         os.makedirs(logs_dir)


    # create_folders()


    # app.worker_config = app.config['STORAGE_WORKER']

    # worker_type = app.worker_config['type']
    # storage_worker = storage_types[worker_type](app)

    # access_log_handler = logging.FileHandler(os.path.join(app.config["LOGS_DIR"], "access.log"))
    # access_log_handler.setLevel(logging.NOTSET)
    # app.logger.addHandler(access_log_handler)


    # @app.before_request
    # def pre_request_logging():
    #     app.logger.info('  '.join([
    #         datetime.today().ctime(),
    #         request.method,
    #         request.url
    #     ])
    #     )
