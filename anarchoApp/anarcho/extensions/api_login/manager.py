from functools import wraps

from flask import current_app, request


class ApiLoginManager(object):
    def __init__(self, app=None, token_header='x-auth-token'):
        self.current_user = None
        self.auth_token_header = token_header
        self._load_user_callback = None
        self._load_user_failed_callback = None
        self.app = app
        if self.app:
            self.init_app(self.app)

    def init_app(self, app):
        """
        Init manager for Flask app
        :param app:
        :type app: Flask
        """
        self.app = app
        app.api_login_manager = self
        # app.after_request(self._drop_user)

    def _drop_user(self, response):
        self.current_user = None

    def load_user(self, callback):
        self._load_user_callback = callback

    def load_user_failed(self, callback):
        self._load_user_failed_callback = callback

    @property
    def user(self):
        auth_token = request.headers.get(self.auth_token_header)
        if auth_token:
            return self._load_user_callback(auth_token)
        else:
            self._load_user_failed_callback()
            return None


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        user = current_app.api_login_manager.user
        if user:
            return func(user, *args, **kwargs)

    return decorated_view
