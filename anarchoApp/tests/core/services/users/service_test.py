import unittest

from anarcho.core.services.users.exceptions import UserAlreadyExist, UserNameLengthIsWrong, \
    PasswordIsTooShort, PasswordIsEmpty, UserNameIsEmpty, EmailFormatIsWrong, EmailIsEmpty
from anarcho.core.services.users.models import User
from anarcho.core.services.users.service import Users
from anarcho.extensions.database.client import DatabaseClient

TEST_USER_NAME = 'user'
TEST_PASSWORD = 'password'
TEST_MAIL = 'user@mail.com'


class TestUsersService(unittest.TestCase):
    def setUp(self):
        config = {
            'SQLALCHEMY_DATABASE_URI': 'sqlite://'
        }
        db = DatabaseClient(config)
        self.user_service = Users(db)

        db.metadata.create_all()

    def test_create_user(self):
        self.user_service.create_user(TEST_MAIL, TEST_PASSWORD, TEST_USER_NAME)
        user = self.user_service.get_user_by_email(TEST_MAIL)
        assert isinstance(user, User)
        assert user

    def create_user_exception_assert(self, expected_exception,
                                     email=TEST_MAIL,
                                     password=TEST_PASSWORD,
                                     name=TEST_USER_NAME):
        with self.assertRaises(expected_exception):
            self.user_service.create_user(email, password, name)

    def test_create_user_already_exist(self):
        self.user_service.create_user(TEST_MAIL, TEST_PASSWORD, TEST_USER_NAME)
        self.create_user_exception_assert(UserAlreadyExist)

    def test_create_user_email_is_empty(self):
        self.create_user_exception_assert(EmailIsEmpty, email='')
        self.create_user_exception_assert(EmailIsEmpty, email='    ')
        self.create_user_exception_assert(EmailIsEmpty, email=None)

    def test_create_user_wrong_email_format(self):
        self.create_user_exception_assert(EmailFormatIsWrong, email='usermail.com')

    def test_create_user_wrong_name_length(self):
        self.create_user_exception_assert(UserNameLengthIsWrong, name='u')

    def test_create_user_name_is_empty(self):
        self.create_user_exception_assert(UserNameIsEmpty, name='')
        self.create_user_exception_assert(UserNameIsEmpty, name='    ')
        self.create_user_exception_assert(UserNameIsEmpty, name=None)

    def test_create_user_pass_too_short(self):
        self.create_user_exception_assert(PasswordIsTooShort, password='pass')

    def test_create_user_pass_is_empty(self):
        self.create_user_exception_assert(PasswordIsEmpty, password='')
        self.create_user_exception_assert(PasswordIsEmpty, password='    ')
        self.create_user_exception_assert(PasswordIsEmpty, password=None)

    def test_get_user_by_email(self):
        expected_user = self.user_service.create_user(TEST_MAIL, TEST_PASSWORD, TEST_USER_NAME)
        actual_user = self.user_service.get_user_by_email(expected_user.email)
        assert isinstance(actual_user, User)
        assert actual_user == expected_user

    def test_get_user_by_id(self):
        expected_user = self.user_service.create_user(TEST_MAIL, TEST_PASSWORD, TEST_USER_NAME)
        actual_user = self.user_service.get_user_by_id(expected_user.id)
        assert isinstance(actual_user, User)
        assert actual_user == expected_user
