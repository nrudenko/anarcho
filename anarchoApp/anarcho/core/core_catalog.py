from objects import AbstractCatalog, Singleton, KwArg

import anarcho

from anarcho.core.services.apps.service import Apps
from anarcho.core.services.storage.service import AppsStorage
from anarcho.core.services.tokens.service import Tokens
from anarcho.core.services.users.service import Users
from anarcho.extensions.database.client import DatabaseClient

config = {'SQLALCHEMY_DATABASE_URI': 'sqlite:///anarcho.db'}
storage_config = {'WORKER': anarcho.core.services.storage.local_storage_worker.LocalStorageWorker}


class App(AbstractCatalog):
    db = Singleton(DatabaseClient,
                   KwArg('config', config))
    """:type: (objects.Provider) -> DatabaseClient"""


class Services(AbstractCatalog):
    """Services catalog."""

    tokens = Singleton(Tokens,
                       KwArg('db', App.db))
    """:type: (objects.Provider) -> Tokens"""

    users = Singleton(Users,
                      KwArg('db', App.db))
    """:type: (objects.Provider) -> Users"""

    apps = Singleton(Apps,
                     KwArg('db', App.db))
    """:type: (objects.Provider) -> Apps"""

    appsStorage = Singleton(AppsStorage,
                            KwArg('config', storage_config))
    """:type: (objects.Provider) -> AppsStorage"""
