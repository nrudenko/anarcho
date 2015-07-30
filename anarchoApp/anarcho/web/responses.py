from flask import jsonify
from flask.helpers import make_response


def json_response(obj):
    return make_response(jsonify(obj.__dict__))


class TokenResponse(object):
    def __init__(self, token):
        """
        Init TokenView model for serialization
        :param token:
        :type token: anarcho.core.services.tokens.models.Token
        """
        self.token = token.value


class UserResponse(object):
    def __init__(self, user):
        """
        Init UserView model for serialization
        :param user:
        :type user: anarcho.core.services.users.models.User
        """
        self.name = user.name
        self.id = user.id


class AppResponse(object):
    def __init__(self, app):
        """
        Init AppView model for serialization
        :param app:
        :type app: anarcho.core.services.apps.models.Application
        """
        self.created_on = app.created_on
        self.app_key = app.app_key
        self.app_type = app.app_type
        self.name = app.name
        self.package = app.package


class AppsListResponse(object):
    def __init__(self, apps):
        """
        Init UserView model for serialization
        :param apps:
        :type apps: anarcho.core.services.users.models.User
        """
        self.list = [AppResponse(app).__dict__ for app in apps]
