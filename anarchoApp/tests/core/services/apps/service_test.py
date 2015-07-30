import unittest

from sqlalchemy import select

from anarcho.core.services.apps.exceptions import AppNotFound

from anarcho.core.services.apps.models import UserApplication, Application
from anarcho.core.services.apps.service import Apps
from anarcho.extensions.database.client import DatabaseClient

FIRST_TEST_APP_NAME = 'first_test_app'
SECOND_TEST_APP_NAME = 'second_test_app'
FIRST_TEST_USER_ID = 1
SECOND_TEST_USER_ID = 2
TEST_APP_KEY = 'test_app_key'


class TestAppsService(unittest.TestCase):
    def setUp(self):
        config = {
            'SQLALCHEMY_DATABASE_URI': 'sqlite://'
        }
        db = DatabaseClient(config)
        self.apps_service = Apps(db)

        db.metadata.create_all()

    def test_create_app(self):
        created_app = self.apps_service.create_app(TEST_APP_KEY, FIRST_TEST_APP_NAME)
        assert isinstance(created_app, Application)
        assert created_app.name == FIRST_TEST_APP_NAME
        assert created_app.app_key == TEST_APP_KEY
        assert created_app.created_on

    def test_link_app_with_user(self):
        created_app = self.apps_service.create_app(TEST_APP_KEY, FIRST_TEST_APP_NAME)
        self.apps_service.link_app_with_user(TEST_APP_KEY, FIRST_TEST_USER_ID)
        linked_app = self.apps_service.get_user_app(FIRST_TEST_USER_ID, created_app.app_key)
        assert isinstance(linked_app, UserApplication)
        assert linked_app.name == FIRST_TEST_APP_NAME
        assert linked_app.app_key == TEST_APP_KEY
        assert linked_app.permissions == 'r'
        assert linked_app.created_on

    def test_add_new_user_app(self):
        created_app = self.apps_service.add_new_user_app(FIRST_TEST_APP_NAME, FIRST_TEST_USER_ID)
        assert isinstance(created_app, UserApplication)
        assert created_app.name == FIRST_TEST_APP_NAME
        assert created_app.app_key
        assert created_app.created_on
        stored_app = self.apps_service.get_user_app(FIRST_TEST_USER_ID, created_app.app_key)
        assert created_app == stored_app

    def test_get_app_not_exist(self):
        with self.assertRaises(AppNotFound):
            self.apps_service.get_user_app(FIRST_TEST_APP_NAME, FIRST_TEST_USER_ID)

    def test_delete_app(self):
        created_app = self.apps_service.add_new_user_app(FIRST_TEST_APP_NAME, FIRST_TEST_USER_ID)
        self.apps_service.link_app_with_user(created_app.app_key, SECOND_TEST_USER_ID)

        self.apps_service.delete_app(created_app.app_key)

        with self.apps_service.db.engine.connect() as connection:
            selection_query = select([self.apps_service.apps])
            apps_rows = connection.execute(selection_query).fetchall()
            assert len(apps_rows) == 0
            selection_query = select([self.apps_service.user_app])
            user_app_rows = connection.execute(selection_query).fetchall()
            assert len(user_app_rows) == 0
