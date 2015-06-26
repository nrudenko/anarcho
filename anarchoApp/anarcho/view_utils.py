import re


class AnarchoApiException(Exception):
    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def __init__(self, exception, status_code=400):
        Exception.__init__(self)
        self.message = self.type_str(exception.__class__)
        self.status_code = status_code

    @staticmethod
    def type_str(clazz):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', clazz.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
