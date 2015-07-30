import re

from sqlalchemy import select, insert

from anarcho.core.services.users import tables
from anarcho.core.services.users.exceptions import UserNameIsEmpty, UserNameLengthIsWrong, EmailIsEmpty, \
    EmailFormatIsWrong, PasswordIsEmpty, PasswordIsTooShort, UserAlreadyExist, UserServiceException, WrongCredentials
from anarcho.core.services.users.models import User
from .secure import generate_password_hash
from anarcho.core.services.users.secure import verify_pass_hash


def assert_name(name):
    if name is None or name.isspace() or len(name) is 0:
        raise UserNameIsEmpty()
    elif len(name) < 3 or len(name) > 20:
        raise UserNameLengthIsWrong()


def assert_password(password):
    if password is None or password.isspace() or len(password) is 0:
        raise PasswordIsEmpty()
    elif len(password) < 6:
        raise PasswordIsTooShort()


def assert_email(email):
    if email is None or email.isspace() or len(email) is 0:
        raise EmailIsEmpty()
    else:
        email = email.lower()
        if not re.match(r'\w[\w\.-]*@\w[\w\.-]+\.\w+', email) or len(email) > 255:
            raise EmailFormatIsWrong()
    return email


class Users(object):
    def __init__(self, db):
        """
        Init users service
        :param db:
        :type db: anarcho.extensions.database.client.DatabaseClient
        :return:
        """
        self.db = db
        self.users = tables.users(db.metadata)

    def create_user(self, email, password, name):
        """
        Creates new user

        :param email: user's email
        :param password: user's password
        :param name: user's name
        :return: created user
        :rtype: .models.User
        """
        assert_name(name)
        assert_email(email)
        assert_password(password)

        email = email.lower()

        user = self.get_user_by_email(email)

        if user:
            raise UserAlreadyExist()
        else:
            user = User(email=email,
                        name=name,
                        pass_hash=generate_password_hash(password))
            self._insert_user(user)
            user = self.get_user_by_email(email)

            if user:
                return user
        raise UserServiceException()

    def _insert_user(self, user):
        """
        Insert user to database

        :param user:
        :type user: User
        """
        with self.db.engine.connect() as connection:
            transaction = connection.begin()
            insert_query = insert(self.users).values(
                email=user.email,
                name=user.name,
                pass_hash=user.pass_hash
            )
            connection.execute(insert_query)
            transaction.commit()

    def get_user_by_id(self, user_id):
        """
        Get user by id
        :param user_id:
        :return: User by id
        :rtype: User
        """
        with self.db.engine.connect() as connection:
            select_query = select([self.users]).where(self.users.c.id == user_id)
            result = connection.execute(select_query).fetchone()
            return User.from_row(result)

    def get_user_by_email(self, email):
        """
        Get user by email
        :param email:
        :return: User by email
        :rtype: User
        """
        with self.db.engine.connect() as connection:
            select_query = select([self.users]).where(self.users.c.email == email)
            result = connection.execute(select_query).fetchone()
            return User.from_row(result)

    def assert_credentials(self, email, password):
        """
        Assert that credentials exist in database
        :param email: user's email
        :param password: user's plain text password
        :raises WrongCredentials: if email or password are not correct
        """
        user = self.get_user_by_email(email)
        if not user or not verify_pass_hash(password, user.pass_hash):
            raise WrongCredentials
        return True
