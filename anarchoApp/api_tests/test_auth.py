import json
from api_tests import AnarchoTestCase

test_user_email = 'test2@mail.com'
test_user_name = 'test_user2'
test_user_password = 'password'


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
        self.assert_error_message(r, 'user_already_registered')

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
        self.assert_error_message(r, 'wrong_credentials')

    def test_get_user(self):
        self.register()
        r = self.login()
        response_data = json.loads(r.data)
        r = self.do_get('/api/user', response_data['authToken'])
        self.assert_status_code(r)

    def test_registration_with_empty_name(self):
        r = self.register(test_user_email, '', test_user_password)
        self.assert_status_code(r, 403)
        self.assert_error_message(r, 'user_name_is_empty')

    def test_registration_with_invalid_name_length(self):
        r = self.register(test_user_email, 'testestestestetstetstetstetstetstets', test_user_password)
        self.assert_status_code(r, 403)
        self.assert_error_message(r, 'invalid_user_name_length')

    def test_registration_with_empty_email(self):
        r = self.register('', test_user_name, test_user_password)
        self.assert_status_code(r, 403)
        self.assert_error_message(r, 'email_is_empty')

    def test_registration_with_invalid_format_email(self):
        r = self.register('asdsd@.com', test_user_name, test_user_password)
        self.assert_status_code(r, 403)
        self.assert_error_message(r, 'invalid_email_format')

    def test_registration_with_invalid_email_length(self):
        r = self.register('qwscvdfg3456ghbsdfdfnmdvcd@cc.com', test_user_name, test_user_password)
        self.assert_status_code(r, 403)
        self.assert_error_message(r, 'invalid_email_length')

    def test_registration_with_empty_password(self):
        r = self.register(test_user_email, test_user_name, ' ')
        self.assert_status_code(r, 403)
        self.assert_error_message(r, 'empty_password')

    def test_registration_with_invalid_password_length(self):
        r = self.register(test_user_email, test_user_name, '123')
        self.assert_status_code(r, 403)
        self.assert_error_message(r, 'invalid_password_length')

    def test_registration_with_insensitive_email(self):
        email = 'TeStEr@MaIl.cOm'
        self.register(email=email, name='tester', password=test_user_password)
        r = self.login(email=email.lower(), password=test_user_password)
        self.assert_status_code(r)
        response_data = json.loads(r.data)
        self.assertTrue('authToken' in response_data, msg='User can not login with insensitive email!')