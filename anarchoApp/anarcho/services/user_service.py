from anarcho.models.token import Token
from anarcho.models.user import User
from anarcho.services.exceptions import UserNameIsEmpty, EmailIsEmpty, EmailFormatIsWrong, PasswordIsEmpty, \
    PasswordIsTooShort, UserAlreadyExist, UserNotAuthorized
from anarcho.services.exceptions import UsernameLengthIsWrong

import re


class UserService(object):
    def __init__(self, db):
        self.db = db

    def _create_token(self, user):
        token = Token(user)
        self.db.session.add(token)
        self.db.session.commit()
        return token

    def create_user(self, name, email, password):
        if name is None or name.isspace():
            raise UserNameIsEmpty()
        elif len(name) < 3 or len(name) > 20:
            raise UsernameLengthIsWrong()

        if email is None or email.isspace():
            raise EmailIsEmpty()
        else:
            email = email.lower()
            if not re.match(r'\w[\w\.-]*@\w[\w\.-]+\.\w+', email) or len(email) > 255:
                raise EmailFormatIsWrong()

        if password is None or password.isspace():
            raise PasswordIsEmpty()
        elif len(password) < 6:
            raise PasswordIsTooShort()

        user = User.query.filter(User.email == email).first()
        if user:
            raise UserAlreadyExist()
        else:
            user = User(email, name, password)
            self.db.session.add(user)
            self.db.session.commit()
            return user

    def authenticate(self, email, password):
        u = User.query.filter(User.email == email).first()
        if u is not None and u.verify_password(password):
            if u.token:
                return u.token
            else:
                return self._create_token(u)
        else:
            raise UserNotAuthorized()
