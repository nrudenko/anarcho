import json
from test import AnarchoTestCase


class AuthTest(AnarchoTestCase):
    def test_registration(self):
        r = self.register()
        self.assert_status_code(r)
        response_data = json.loads(r.data)
        self.assertTrue('authToken' in response_data, msg='authToken not in response data')

    def test_registration_already_registered(self):
        self.register()
        r = self.register()
        self.assert_status_code(r, 409)

    def test_login(self):
        self.register()
        r = self.login()
        self.assert_status_code(r)
        response_data = json.loads(r.data)
        self.assertTrue('authToken' in response_data, msg='authToken not in response data')

    def test_login_wrong_credentials(self):
        self.register()
        r = self.login(email='wrong@mail.com')
        self.assert_status_code(r, 403)

    def test_get_user(self):
        self.register()
        r = self.login()
        response_data = json.loads(r.data)
        r = self.get_json('/api/user', response_data['authToken'])
        self.assert_status_code(r)