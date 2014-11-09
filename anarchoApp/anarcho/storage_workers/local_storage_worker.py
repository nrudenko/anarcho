import shutil
from anarcho.storage_workers.base_worker import BaseStorageWorker
from flask import send_file
import os


class LocalStorageWorker(BaseStorageWorker):
    def __init__(self, flask_app):
        super(LocalStorageWorker, self).__init__(flask_app)

        if 'storage_dir' not in self.flask_app.worker_config:
            raise Exception("Your app should have storage_dir in STORAGE_WORKER config")

    def get_app_dir(self, app_key):
        local_storage_dir = self.flask_app.worker_config['storage_dir']
        return os.path.join(local_storage_dir, app_key)

    def get_build_path(self, build):
        return os.path.join(self.get_app_dir(build.app_key), str(build.id) + ".apk")

    def get_icon_path(self, app_key):
        return os.path.join(self.get_app_dir(app_key), "icon.png")

    def put(self, build, tmp_apk_path, tmp_icon_path):
        new_path = self.get_build_path(build)
        new_path_dir = os.path.dirname(new_path)

        if not os.path.exists(new_path_dir):
            os.makedirs(new_path_dir)

        shutil.copy(tmp_apk_path, new_path)
        shutil.copy(tmp_icon_path, self.get_icon_path(build.app_key))

    def get(self, build):
        return send_file(self.get_build_path(build))

    def get_main_url(self):
        host_name = self.flask_app.worker_config['storage_host_name']
        return str(host_name + "/api/").replace("//api", "/api")

    def get_build_link(self, build):
        return self.get_main_url() + "build/%s/%d" % (build.app_key, build.id)

    def get_icon_link(self, app_key):
        return self.get_main_url() + "icon/%s" % app_key

    def remove(self, build):
        path = self.get_build_path(build)
        if os.path.exists(path):
            os.remove(path)