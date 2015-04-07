import time
import re

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from anarcho import db
from anarcho.reasons import errors
from anarcho.models.token import Token


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    pass_hash = Column(String)
    email = Column(String(50), unique=True)
    registered_on = Column(Integer)

    apps = relationship("Application", secondary="users_apps", backref="users")
    token = relationship("Token", uselist=False, backref="users")

    def __init__(self, email=None, name=None, password=None):
        self.email = email
        self.name = name
        if self.name is not None and password is not None:
            self.name = name
            self.hash_password(password)
            self.registered_on = time.time()

    def __repr__(self):
        return '<User %r>' % self.name

    def hash_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_hash, password)

    @classmethod
    def register(cls, name, email, password):
        """
        Create new user or activate invited.

        :param str name:
        :param str email:
        :param str password:
        :return:
        """

        # Check name
        if name.isspace():
            raise ValueError(errors.USER_NAME_IS_EMPTY)
        elif not 1 < len(name) < 20:
            raise ValueError(errors.INVALID_USER_NAME_LENGTH)

        # Check email
        if email.isspace():
            raise ValueError(errors.EMAIL_IS_EMPTY)
        elif not 5 < len(email) < 50:
            raise ValueError(errors.INVALID_EMAIL_LENGTH)
        elif not re.search(r'\w[\w\.-]*@\w[\w\.-]+\.\w+', email):
            raise ValueError(errors.INVALID_EMAIL_FORMAT)

        # Check password
        if password.isspace():
            raise ValueError(errors.EMPTY_PASSWORD)
        elif not 5 < len(password) < 100:
            raise ValueError(errors.INVALID_PASSWORD_LENGTH)

        email = email.lower()

        # Find the same user
        user = cls.query.filter(cls.email == email).first()

        if user and user.name:
            raise ValueError(errors.USER_ALREADY_REGISTERED)

        if not user:
            # Create new
            user = cls(email, name, password)
            db.session.add(user)
            db.session.commit()
        else:
            # Activate invited
            user.name = name
            user.hash_password(password)
            db.session.commit()

        token = Token(user)
        db.session.add(token)
        db.session.commit()

        return token
