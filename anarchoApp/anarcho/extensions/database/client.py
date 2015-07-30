"""Database."""

from sqlalchemy import MetaData
from sqlalchemy.engine import create_engine


class DatabaseClient(object):
    """Database client."""

    engine = None
    """:type engine: sqlalchemy.engine.Engine"""

    metadata = None
    """:type session: sqlalchemy.MetaData"""

    def __init__(self, config={}):
        """Initializer.
        """
        self.engine = None
        self.metadata = None
        self.config = config
        if config:
            self.update_config(config)

    def update_config(self, config):
        """Initialize extension.

        :type app:
        :return:
        """
        self.config = config
        self.engine = create_engine(self.config['SQLALCHEMY_DATABASE_URI'])
        self.metadata = MetaData(bind=self.engine)
