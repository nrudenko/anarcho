from time import sleep
import unittest

from anarcho.core.services.tokens.models import Token
from anarcho.core.services.tokens.service import Tokens
from anarcho.extensions.database.client import DatabaseClient

TEST_AUTH_ID = 'user@mail.com'


class TestUsersService(unittest.TestCase):
    def setUp(self):
        config = {
            'SQLALCHEMY_DATABASE_URI': 'sqlite://'
        }
        db = DatabaseClient(config)
        self.tokens_service = Tokens(db)

        db.metadata.create_all()

    def test_create_token(self):
        token = self.tokens_service.create_token(TEST_AUTH_ID)
        assert token
        assert token.auth_id == TEST_AUTH_ID
        assert token.value

    def test_get_token_by_value(self):
        expected_token = self.tokens_service.create_token(TEST_AUTH_ID)
        actual_token = self.tokens_service.get_token_by_value(expected_token.value)
        assert actual_token
        assert isinstance(actual_token, Token)
        assert expected_token == actual_token

    def test_is_token_expired_true(self):
        self.tokens_service.expiration_time = 1
        token = self.tokens_service.create_token(TEST_AUTH_ID)
        sleep(2 / 1000)
        assert self.tokens_service.is_token_expired(token.value)

    def test_is_token_expired_false(self):
        self.tokens_service.expiration_time = 3
        token = self.tokens_service.create_token(TEST_AUTH_ID)
        sleep(2 / 1000)
        assert not self.tokens_service.is_token_expired(token.value)
