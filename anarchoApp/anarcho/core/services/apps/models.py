from anarcho.core.services.data_model import DataModel


class Application(DataModel):
    def __init__(self, **kwargs):
        self.id = None
        self.name = None
        self.package = None
        self.app_key = None
        self.created_on = None
        self.app_type = None
        super(Application, self).__init__(**kwargs)


class UserApplication(Application):
    def __init__(self, **kwargs):
        self.permissions = None
        super(UserApplication, self).__init__(**kwargs)
