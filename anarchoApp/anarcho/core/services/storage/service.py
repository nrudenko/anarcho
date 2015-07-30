class AppsStorage(object):
    def __init__(self, config):
        super(AppsStorage, self).__init__()
        worker_clz = config.get('WORKER')
        if worker_clz:
            self.worker = worker_clz(config)
        else:
            raise RuntimeError('TROLOLO BLIN NAFIK')
            # todo replace with normal exception

    def get_app_icon(self, app_key):
        self.worker.get(app_key + '/icon')

    def remove_app(self, app_key):
        self.worker.remove_object(app_key)

    def remove_app(self, app_key, build_id):
        self.worker.remove_object(app_key + '/' + build_id)

    def store_build(self, build_file, app_key, build_id):
        self.worker.put(build_file, app_key + '/' + build_id)


        # def get_app_dir(self, app_key):
        #      local_storage_dir = self.config['local_storage_dir']
        #      return os.path.join(local_storage_dir, app_key)
        #
        #  def get_build_path(self, build):
        #      from anarcho.app.models.application import IOS, ANDR
        #
        #      ext = None
        #      if build.app.app_type == IOS:
        #          ext = 'ios'
        #      elif build.app.app_type == ANDR:
        #          ext = 'apk'
        #      return os.path.join(self.get_app_dir(build.app_key), str(build.id) + "." + ext)
        #
        #  def get_icon_path(self, app_key):
        #      return os.path.join(self.get_app_dir(app_key), "icon.png")
        #
        #  def put(self, build, tmp_build_path, tmp_icon_path):
        #      new_path = self.get_build_path(build)
        #      new_path_dir = os.path.dirname(new_path)
        #
        #      if not os.path.exists(new_path_dir):
        #          os.makedirs(new_path_dir)
        #
        #      shutil.copy(tmp_build_path, new_path)
        #      if tmp_icon_path:
        #          shutil.copy(tmp_icon_path, self.get_icon_path(build.app_key))
        #
        #  def get(self, build):
        #      return self.get_build_path(build)
        #
        #  def get_main_url(self, https=False):
        #      if https:
        #          if 'local_storage_host_https' in self.config:
        #              host_name = self.config['local_storage_host_https']
        #      else:
        #          if 'local_storage_host' in self.config:
        #              host_name = self.config['local_storage_host']
        #      return str(host_name + "/api/").replace("//api", "/api")
        #
        #  def get_build_link(self, build):
        #      from anarcho.app.models.application import IOS, ANDR
        #
        #      if build.app.app_type == IOS:
        #          return self.get_main_url(https=True) + "apps/%s/%d/file" % (build.app_key, build.id)
        #      elif build.app.app_type == ANDR:
        #          return self.get_main_url() + "apps/%s/%d/file" % (build.app_key, build.id)
        #
        #  def get_icon_link(self, app_key):
        #      return self.get_main_url() + "icon/%s" % app_key
        #
        #  def remove_build(self, build):
        #      path = self.get_build_path(build)
        #      if os.path.exists(path):
        #          os.remove(path)
        #
        #  def remove_app(self, app):
        #      path = self.get_app_dir(app.app_key)
        #      if os.path.exists(path):
        #          shutil.rmtree(path)
