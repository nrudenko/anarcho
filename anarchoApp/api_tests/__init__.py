import json
from unittest import TestCase

import anarcho
from anarcho.models.application import Application
import config_module
import os


class AnarchoREST(TestCase):
    def make_client(self):
        self.client = anarcho.app.test_client()
        self.token = None

    def prepare_headers(self, auth_token):
        self.headers = [('Content-Type', 'application/json')]
        if auth_token is not None:
            self.headers.append(('x-auth-token', auth_token))
        elif self.token is not None:
            self.headers.append(('x-auth-token', self.token))

    def do_get(self, end_point, auth_token=None):
        self.prepare_headers(auth_token)
        return self.client.get(end_point,
                               headers=self.headers)

    def do_post(self, end_point, params, auth_token=None):
        self.prepare_headers(auth_token)
        return self.client.post(end_point,
                                headers=self.headers,
                                data=json.dumps(params))

    def do_delete(self, end_point, params, auth_token=None):
        self.prepare_headers(auth_token)
        return self.client.delete(end_point,
                                  headers=self.headers,
                                  data=json.dumps(params))

    def do_patch(self, end_point, params, auth_token=None):
        self.prepare_headers(auth_token)
        return self.client.patch(end_point,
                                 headers=self.headers,
                                 data=json.dumps(params))


class AnarchoTestCase(AnarchoREST):
    test_user_email = 'test@mail.com'
    test_user_name = 'test_name'
    test_user_password = 'password'

    def setUp(self):
        AnarchoREST.make_client(self)
        config_path = os.path.join(os.path.dirname(config_module.__file__), "test_config.py")
        anarcho.init_config(config_path)
        anarcho.db.create_all()
        self.created_app = None

    def tearDown(self):
        anarcho.db.drop_all()

    def assert_status_code(self, r, code=200):
        self.assertEquals(r.status_code, code, msg='Statuse code {0}'.format(r.status_code))

    def assert_error_message(self, response, message):
        response_data = json.loads(response.data)
        self.assertTrue(message in response_data['error'], msg='Bad validation error message!')

    def register(self, email=test_user_email, name=test_user_name, password=test_user_password):
        params = dict(email=email, name=name, password=password)
        return self.do_post('/api/register', params)

    def login(self, email=test_user_email, password=test_user_password):
        params = dict(email=email, password=password)
        r = self.do_post('/api/login', params)
        response_data = json.loads(r.data)
        if 'authToken' in response_data:
            self.token = response_data['authToken']
        return r

    def create_app(self, app_name='test_app'):
        params = {'name': app_name}
        r = self.do_post('/api/apps', params)
        app_key = json.loads(r.data)['app_key']
        self.created_app = Application.query.filter_by(app_key=app_key).first()
        return r

    def add_to_team(self, email=test_user_email, app_key='app_key', permission='w'):
        params = {'email': email,
                  'app_key': app_key,
                  'permission': permission}
        return self.do_post('/api/permission', params)

    def update_permission(self, email=test_user_email, app_key='app_key', permission='w'):
        params = {'email': email,
                  'app_key': app_key,
                  'permission': permission}
        return self.do_patch('/api/permission', params)

    def remove_permission(self, email=test_user_email, app_key='app_key'):
        params = {'email': email,
                  'app_key': app_key}
        return self.do_delete('/api/permission', params)