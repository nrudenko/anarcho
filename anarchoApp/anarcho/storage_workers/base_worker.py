class BaseStorageWorker(object):
    def __init__(self, flask_app):
        self.flask_app = flask_app

    def put(self, build, tmp_build_path, tmp_icon_path):
        pass

    def get(self, build):
        pass

    def get_build_link(self, build):
        pass

    def get_icon_link(self, app_key):
        pass

    def remove(self, build):
        pass