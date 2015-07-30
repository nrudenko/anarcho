class BaseStorageWorker(object):
    def __init__(self, config):
        self.config = config

    def put(self, file_object, key):
        pass

    def get(self, key):
        pass

    def remove_object(self, build):
        pass
