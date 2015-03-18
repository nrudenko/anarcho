import shutil

from anarcho import app
from anarcho.storage_workers.base_worker import BaseStorageWorker
import os


class LocalStorageWorker(BaseStorageWorker):
    def __init__(self, flask_app):
        super(LocalStorageWorker, self).__init__(flask_app)

        if 'local_storage_dir' not in self.flask_app.worker_config:
            raise Exception("Absent local_storage_dir in STORAGE_WORKER config")
        if 'local_storage_host' not in self.flask_app.worker_config:
            raise Exception("Absent local_storage_host in STORAGE_WORKER config")
        if 'local_storage_host_https' not in self.flask_app.worker_config:
            raise Exception("Absent local_storage_host_https in STORAGE_WORKER config")

    def get_app_dir(self, app_key):
        local_storage_dir = self.flask_app.worker_config['local_storage_dir']
        return os.path.join(local_storage_dir, app_key)

    def get_build_path(self, build):
        from anarcho.models.application import IOS, ANDR

        ext = None
        if build.app.app_type == IOS:
            ext = 'ios'
        elif build.app.app_type == ANDR:
            ext = 'apk'
        return os.path.join(self.get_app_dir(build.app_key), str(build.id) + "." + ext)

    def get_icon_path(self, app_key):
        return os.path.join(self.get_app_dir(app_key), "icon.png")

    def put(self, build, tmp_build_path, tmp_icon_path):
        new_path = self.get_build_path(build)
        new_path_dir = os.path.dirname(new_path)

        if not os.path.exists(new_path_dir):
            os.makedirs(new_path_dir)

        shutil.copy(tmp_build_path, new_path)
        if tmp_icon_path:
            shutil.copy(tmp_icon_path, self.get_icon_path(build.app_key))

    def get(self, build):
        return self.get_build_path(build)

    def get_main_url(self, https=False):
        if https:
            if 'local_storage_host_https' in self.flask_app.worker_config:
                host_name = self.flask_app.worker_config['local_storage_host_https']
            else:
                host_name = app.config['PUBLIC_HOST_SECURE']
        else:
            if 'local_storage_host' in self.flask_app.worker_config:
                host_name = self.flask_app.worker_config['local_storage_host']
            else:
                host_name = app.config['PUBLIC_HOST']
        return str(host_name + "/api/").replace("//api", "/api")

    def get_build_link(self, build):
        from anarcho.models.application import IOS, ANDR

        if build.app.app_type == IOS:
            return self.get_main_url(https=True) + "apps/%s/%d/file" % (build.app_key, build.id)
        elif build.app.app_type == ANDR:
            return self.get_main_url() + "apps/%s/%d/file" % (build.app_key, build.id)

    def get_icon_link(self, app_key):
        return self.get_main_url() + "icon/%s" % app_key

    def remove_build(self, build):
        path = self.get_build_path(build)
        if os.path.exists(path):
            os.remove(path)

    def remove_app(self, app):
        path = self.get_app_dir(app.app_key)
        if os.path.exists(path):
            shutil.rmtree(path)