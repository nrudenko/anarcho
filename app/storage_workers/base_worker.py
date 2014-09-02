class BaseStorageWorker(object):
    def __init__(self, flask_app):
        self.flask_app = flask_app

    def put(self, build, tmp_apk_path, tmp_icon_path):
        pass

    def get(self, build):
        pass

    def get_build_link(self, build):
        pass

    def get_icon_link(self, build):
        pass

    def remove(self, build):
        pass