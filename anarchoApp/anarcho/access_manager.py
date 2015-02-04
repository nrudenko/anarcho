from functools import wraps
import hmac

from flask import request, make_response, g, current_app, Response


permissions = ['r', 'w', 'u']


def _secret_key(key=None):
    if key is None:
        key = current_app.config['SECRET_KEY']

    if isinstance(key, unicode):  # pragma: no cover
        key = key.encode('latin1')  # ensure bytes

    return key


def make_secure_token(*args, **options):
    '''
    This will create a secure token that you can use as an authentication
    token for your users. It uses heavy-duty HMAC encryption to prevent people
    from guessing the information. (To make it even more effective, if you
    will never need to regenerate the token, you can  pass some random data
    as one of the arguments.)
    :param \*args: The data to include in the token.
    :type args: args
    :param \*\*options: To manually specify a secret key, pass ``key=THE_KEY``.
        Otherwise, the ``current_app`` secret key will be used.
    :type \*\*options: kwargs
    '''
    key = options.get('key')
    key = _secret_key(key)

    l = [s if isinstance(s, bytes) else s.encode('utf-8') for s in args]

    payload = b'\0'.join(l)

    token_value = hmac.new(key, payload).hexdigest()

    if hasattr(token_value, 'decode'):  # pragma: no cover
        token_value = token_value.decode('utf-8')  # ensure bytes

    return token_value


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):

        if 'x-auth-token' in request.headers:
            token = request.headers['x-auth-token']
            from anarcho.models.token import Token

            t = Token.query.filter_by(auth_token=token).first()
            if t is not None:
                g.user = t.user
                return func(*args, **kwargs)

        return Response('{"error":"unauthorized"}', 401, {'WWWAuthenticate': 'Basic realm="Login Required"'})

    return decorated_view


def app_permissions(permissions=[]):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            from anarcho.models.user_app import UserApp

            json = request.json if hasattr(request, 'json') else None

            if json is not None and 'app_key' in json:
                app_key = json['app_key']
            elif 'app_key' in kwargs:
                app_key = kwargs['app_key']
            else:
                raise ValueError("app_permissions : wrapped function should have"
                                 " app_key in args or in request.json")
            user = g.user
            result = make_response('{"error":"not_enough_permission"}', 403)
            if user is not None:
                user_app = UserApp.query.filter_by(app_key=app_key, user_id=user.id).first()
                if user_app.permission in permissions:
                    result = func(*args, **kwargs)
            return result

        return decorated_view

    return decorator


def is_permission_allowed(permission):
    return permission in permissions