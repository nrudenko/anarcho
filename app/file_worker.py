import os


class BaseStorageWorker():
    def __init__(self, flask_app):
        self.flask_app = flask_app

    def put(self, build, build_file):
        pass

    def get_path(self, build):
        pass

    def remove(self, build):
        pass


class LocalStorageWorker(BaseStorageWorker):
    def get_build_path(self, build):
        return os.path.join(self.flask_app.config['UPLOAD_FOLDER'], build.app_key, str(build.id) + ".apk")

    def put(self, build, build_file):
        new_path = self.get_build_path(build)
        new_path_dir = os.path.dirname(new_path)

        tmp_path = os.path.abspath(build_file)
        print new_path, tmp_path

        if not os.path.exists(new_path_dir):
            os.makedirs(new_path_dir)
        os.rename(tmp_path, new_path)

    def get_path(self, build):
        build_path = self.get_build_path(build)
        return build_path