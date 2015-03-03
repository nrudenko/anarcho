from test import AnarchoTestCase

from anarcho.models.user import User
from anarcho.models.user_app import UserApp


test_team_user_email = 'test2@mail.com'
test_team_user_name = 'test_name2'


class TeamTest(AnarchoTestCase):
    def setUp(self):
        AnarchoTestCase.setUp(self)
        self.register()
        self.login()
        self.register(email=test_team_user_email, name=test_team_user_name)
        self.create_app()
        self.app_key = self.created_app.app_key
        self.add_to_team(email=test_team_user_email, app_key=self.app_key, permission='r')

    def get_user_app(self):
        """
        :rtype: UserApp
        """
        user = User.query.filter_by(email=test_team_user_email).first()
        if user:
            return UserApp.query.filter_by(user_id=user.id).first()

    def test_permissions_update(self):
        r = self.update_permission(email=test_team_user_email, app_key=self.app_key, permission='w')
        self.assert_status_code(r)
        user_app = self.get_user_app()
        self.assertIsNotNone(user_app, msg='UserApp for {0} not found'.format('test2@mail.com'))
        self.assertTrue(user_app.permission == 'w', msg='Wrong permission after update')

    def test_permissions_remove(self):
        r = self.remove_permission(email=test_team_user_email, app_key=self.app_key)
        self.assert_status_code(r)
        user_app = self.get_user_app()
        self.assertIsNone(user_app, msg='UserApp for {0} not deleted'.format('test2@mail.com'))

    def test_user_can_not_remove_his_permissions(self):
        r = self.remove_permission(email=self.test_user_email, app_key=self.app_key)
        self.assert_status_code(r, 403)

    def test_user_can_not_update_his_permissions(self):
        r = self.remove_permission(email=self.test_user_email, app_key=self.app_key)
        self.assert_status_code(r, 403)

    def test_user_can_not_add_to_app_existing_user(self):
        r = self.register(email=test_team_user_email, name='test_name2')
        self.assert_status_code(r, 409)

    def test_email_format_validation(self):
        r = self.add_to_team(email='test3mail.com', app_key=self.app_key, permission='r')
        self.assert_status_code(r, 403)

    def test_empty_email_validation(self):
        r = self.add_to_team(email=' ', app_key=self.app_key, permission='r')
        self.assert_status_code(r, 403)

    def test_email_length_validation(self):
        r = self.add_to_team(email='asdcvbnftewscmbpdtv@mail.com', app_key=self.app_key, permission='r')
        self.assert_status_code(r, 403)

    def test_add_existing_user_to_team(self):
        self.register('test3@mail.com', 'test_name3')
        self.create_app(app_name='test_app2')
        self.login()
        r = self.add_to_team(email='test3@mail.com', app_key=self.app_key, permission='r')
        self.assert_status_code(r)