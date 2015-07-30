import datetime
import hmac
import uuid

from sqlalchemy import select, insert

from anarcho.core.services.tokens import tables
from anarcho.core.services.tokens.models import Token

FIFTEEN_DAYS = 15 * 24 * 60 * 60 * 1000


def _generate_token_value():
    """
    Generate random secure token value
    :return: token value
    :rtype: str
    """
    key = str(uuid.uuid4())
    l = [s if isinstance(s, bytes) else s.encode('utf-8') for s in key]
    payload = b'\0'.join(l)
    token_value = hmac.new(key, payload).hexdigest()
    if hasattr(token_value, 'decode'):  # pragma: no cover
        token_value = token_value.decode('utf-8')  # ensure bytes

    return token_value


def _next_expiration_date(expiration_interval):
    """
    Append expiration_interval to current date
    :param expiration_interval:
    :type expiration_interval: int
    :return: time in future increased with expiration_interval value
    :rtype: datetime.datetime
    """
    return datetime.datetime.now() + datetime.timedelta(milliseconds=expiration_interval)


class Tokens(object):
    def __init__(self, db):
        """
        AuthService init

        """
        self.db = db
        self.tokens = tables.tokens(db.metadata)

    def get_token_by_value(self, value):
        """
        Find Token by value
        :param value:
        :type value: str
        :return: Token
        :rtype: Token
        """
        with self.db.engine.connect() as connection:
            select_query = select([self.tokens]).where(self.tokens.c.value == value)
            result = connection.execute(select_query).fetchone()
            return Token.from_row(result)

    def get_token_by_auth_id(self, auth_id):
        """
        Find Token by auth_id
        :param auth_id:
        :type auth_id: str
        :return: Token
        :rtype: Token
        """
        with self.db.engine.connect() as connection:
            select_query = select([self.tokens]).where(self.tokens.c.auth_id == auth_id)
            result = connection.execute(select_query).fetchone()
            return Token.from_row(result)

    def create_token(self, auth_id, expiration_time=FIFTEEN_DAYS):
        """
        Create token for auth_id
        :param auth_id:
        :type auth_id:str
        :return:
        :rtype: Token
        """
        value = _generate_token_value()
        with self.db.engine.connect() as connection:
            transaction = connection.begin()
            insert_query = insert(self.tokens).values(
                auth_id=auth_id,
                value=value,
                expires_on=_next_expiration_date(expiration_time)
            )
            connection.execute(insert_query)
            transaction.commit()
        return self.get_token_by_value(value)

    def is_token_expired(self, value):
        """
        Verify that token already expired
        :param value: token value
        :return:
        """
        token = self.get_token_by_value(value)
        if token:
            return datetime.datetime.now() >= token.expires_on
