# user_service related exceptions
class UserServiceException(Exception):
    def __init__(self, *args, **kwargs):
        super(UserServiceException, self).__init__(*args, **kwargs)


class UserNameIsEmpty(UserServiceException):
    def __init__(self, *args, **kwargs):
        super(UserNameIsEmpty, self).__init__(*args, **kwargs)


class UsernameLengthIsWrong(UserServiceException):
    def __init__(self, *args, **kwargs):
        super(UsernameLengthIsWrong, self).__init__(*args, **kwargs)


class EmailIsEmpty(UserServiceException):
    def __init__(self, *args, **kwargs):
        super(EmailIsEmpty, self).__init__(*args, **kwargs)


class EmailFormatIsWrong(UserServiceException):
    def __init__(self, *args, **kwargs):
        super(EmailFormatIsWrong, self).__init__(*args, **kwargs)


class PasswordIsEmpty(UserServiceException):
    def __init__(self, *args, **kwargs):
        super(PasswordIsEmpty, self).__init__(*args, **kwargs)


class PasswordIsTooShort(UserServiceException):
    def __init__(self, *args, **kwargs):
        super(PasswordIsTooShort, self).__init__(*args, **kwargs)


class UserAlreadyExist(UserServiceException):
    def __init__(self, *args, **kwargs):
        super(UserAlreadyExist, self).__init__(*args, **kwargs)


class UserNotAuthorized(UserServiceException):
    def __init__(self, *args, **kwargs):
        super(UserNotAuthorized, self).__init__(*args, **kwargs)
