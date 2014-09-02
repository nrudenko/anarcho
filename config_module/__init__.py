import os


class DefaultConfig(object):
    TMP_DIR = os.path.abspath("tmp")
    SECRET_KEY = os.urandom(24)
    USERNAME = "admin"
    PASSWORD = "admin"
    SQLALCHEMY_DATABASE_URI = "sqlite:///anarcho.db"

    STORAGE_WORKER = "local_storage"
    LOCAL_STORAGE_DIR = "builds"
    STORAGE_HOST_NAME = "http://54.164.28.98"


class DevConfig(DefaultConfig):
    STORAGE_HOST_NAME = "http://localhost:5000"
    DEBUG = True
