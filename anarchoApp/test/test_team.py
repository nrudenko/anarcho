from test import AnarchoTestCase

from anarcho.models.user import User
from anarcho.models.user_app import UserApp


class AuthTest(AnarchoTestCase):
    def setUp(self):
        AnarchoTestCase.setUp(self)
        self.make_auth()
        self.register(email='test2@mail.com', name='test_name2')
        self.create_app()
        self.app_key = self.created_app.app_key
        self.add_to_team(email='test2@mail.com', app_key=self.app_key, permission='r')

    def get_user_app(self):
        """
        :rtype: UserApp
        """
        user = User.query.filter_by(email='test2@mail.com').first()
        if user:
            return UserApp.query.filter_by(user_id=user.id).first()

    def test_permissions_update(self):
        r = self.update_permission(email='test2@mail.com', app_key=self.app_key, permission='w')
        self.assert_status_code(r)
        user_app = self.get_user_app()
        self.assertIsNotNone(user_app, msg='UserApp for {0} not found'.format('test2@mail.com'))
        self.assertTrue(user_app.permission == 'w', msg='Wrong permission after update')

    def test_permissions_remove(self):
        r = self.remove_permission(email='test2@mail.com', app_key=self.app_key)
        self.assert_status_code(r)
        user_app = self.get_user_app()
        self.assertIsNone(user_app, msg='UserApp for {0} not deleted'.format('test2@mail.com'))