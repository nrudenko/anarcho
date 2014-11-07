from functools import wraps
from anarcho.models.user_app import UserApp

from flask import request, make_response, g


def app_permissions(permissions=[]):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            json = request.json
            if json is not None and 'app_key' in json:
                app_key = request.json['app_key']
            elif 'app_key' in kwargs:
                app_key = kwargs['app_key']
            else:
                raise ValueError("app_permissions : wrapped function should have"
                                 " app_key in args or in request.json")
            user = g.user
            result = make_response('{"error":"not_enough_permission"}', 403)
            if user is not None:
                user_app = UserApp.query.filter_by(app_key=app_key, email=user.email).first()
                if user_app.permission in permissions:
                    result = func(*args, **kwargs)
            return result

        return decorated_view

    return decorator
