from anarcho.core.services.data_model import DataModel


class Token(DataModel):
    def __init__(self, **kwargs):
        """
        Token initializer
        :param kwargs:
        :return:
        """
        self.id = None
        self.auth_id = None
        self.value = None
        self.expires_on = None
        self.created_on = None
        super(Token, self).__init__(**kwargs)
