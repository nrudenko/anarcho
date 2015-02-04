import json
import unittest

import anarcho
from anarcho.models.application import Application


class AnarchoTestCase(unittest.TestCase):
    def setUp(self):
        self.token = None
        self.created_app = None
        self.app = anarcho.app.test_client()
        anarcho.db.create_all()

    def tearDown(self):
        anarcho.db.drop_all()

    def assert_status_code(self, r, code=200):
        self.assertEquals(r.status_code, code, msg='Statuse code {0}'.format(r.status_code))

    def prepare_headers(self, auth_token):
        self.headers = [('Content-Type', 'application/json')]
        if auth_token is not None:
            self.headers.append(('x-auth-token', auth_token))
        elif self.token is not None:
            self.headers.append(('x-auth-token', self.token))

    def post_json(self, end_point, params, auth_token=None):
        self.prepare_headers(auth_token)
        return self.app.post(end_point,
                             headers=self.headers,
                             data=json.dumps(params))

    def delete(self, end_point, params, auth_token=None):
        self.prepare_headers(auth_token)
        return self.app.delete(end_point,
                               headers=self.headers,
                               data=json.dumps(params))

    def patch_json(self, end_point, params, auth_token=None):
        self.prepare_headers(auth_token)
        return self.app.patch(end_point,
                              headers=self.headers,
                              data=json.dumps(params))

    def get_json(self, end_point, auth_token=None):
        self.prepare_headers(auth_token)
        return self.app.get(end_point,
                            headers=self.headers)

    def register(self, email='test@mail.com', name='test_name', password='password'):
        params = dict(email=email, name=name, password=password)
        return self.post_json('/api/register', params)

    def login(self, email='test@mail.com', password='password'):
        params = dict(email=email, password=password)
        return self.post_json('/api/login', params)

    def make_auth(self, email='test@mail.com', name='test_name', password='password'):
        r = self.register(email=email, name=name, password=password)
        self.token = json.loads(r.data)['authToken']

    def create_app(self, app_name='test_app'):
        params = {'name': app_name}
        r = self.post_json('/api/apps', params)
        app_key = json.loads(r.data)['app_key']
        self.created_app = Application.query.filter_by(app_key=app_key).first()
        return r

    def add_to_team(self, email='test2@mail.com', app_key='app_key', permission='w'):
        params = {'email': email,
                  'app_key': app_key,
                  'permission': permission}
        return self.post_json('/api/permission', params)

    def update_permission(self, email='test2@mail.com', app_key='app_key', permission='w'):
        params = {'email': email,
                  'app_key': app_key,
                  'permission': permission}
        return self.patch_json('/api/permission', params)

    def remove_permission(self, email='test2@mail.com', app_key='app_key'):
        params = {'email': email,
                  'app_key': app_key}
        return self.delete('/api/permission', params)