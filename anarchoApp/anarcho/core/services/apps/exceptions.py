"""AppsService related exceptions"""


class AppsServiceException(Exception):
    def __init__(self, *args, **kwargs):
        super(AppsServiceException, self).__init__(*args, **kwargs)


class AppNotFound(AppsServiceException):
    def __init__(self, *args, **kwargs):
        super(AppNotFound, self).__init__(*args, **kwargs)
