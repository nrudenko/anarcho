from anarcho.core.services.data_model import DataModel


class User(DataModel):
    def __init__(self, **kwargs):
        self.id = None
        self.name = None
        self.pass_hash = None
        self.email = None
        self.created_on = None
        super(User, self).__init__(**kwargs)
