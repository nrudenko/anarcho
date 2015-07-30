import uuid

from sqlalchemy import insert, select, join, delete

from anarcho.core.services.apps import tables
from anarcho.core.services.apps.exceptions import AppNotFound
from anarcho.core.services.apps.models import Application, UserApplication


class Apps(object):
    def __init__(self, db):
        """
        Init apps service
        :param db:
        :type db: anarcho.extensions.database.client.DatabaseClient
        :return:
        """
        self.db = db
        self.apps = tables.apps(db.metadata)
        self.user_app = tables.user_app(db.metadata)

    def _get_user_app_query(self, where):
        joined_apps = join(self.user_app, self.apps,
                           self.apps.c.app_key == self.user_app.c.app_key)
        select_query = select([self.apps, self.user_app.c.permissions]).select_from(joined_apps).where(where)

        return select_query

    def get_user_apps(self, user_id):
        """
        Return apps list which related to user_id
        :param user_id:
        :type user_id: int
        :return: user's apps
        :rtype: list
        """
        with self.db.engine.connect() as connection:
            select_query = self._get_user_app_query(self.user_app.c.user_id == user_id)
            result = connection.execute(select_query).fetchall()
            return [UserApplication.from_row(row) for row in result]

    def get_user_app(self, user_id, app_key):
        """
        Return app by app_key which related to user_id
        :param user_id:
        :type user_id: int
        :return: user's apps
        :rtype: UserApplication
        """
        with self.db.engine.connect() as connection:
            select_query = self._get_user_app_query(
                self.user_app.c.user_id == user_id and self.user_app.c.app_key == app_key)
            result = connection.execute(select_query).fetchone()
            if result:
                return UserApplication.from_row(result)
            else:
                raise AppNotFound()

    def create_app(self, app_key, name):
        """
        Insert new row to
        :param app_key:
        :param name:
        :return:
        """
        with self.db.engine.connect() as connection:
            transaction = connection.begin()
            insert_app = insert(self.apps).values(
                name=name,
                app_key=app_key,
            )
            connection.execute(insert_app)
            transaction.commit()
        return self.get_app_by_key(app_key)

    def delete_app(self, app_key):
        with self.db.engine.connect() as connection:
            transaction = connection.begin()
            delete_query = delete(self.apps).where(self.apps.c.app_key == app_key)
            connection.execute(delete_query)
            delete_query = delete(self.user_app).where(self.user_app.c.app_key == app_key)
            connection.execute(delete_query)
            transaction.commit()

    def link_app_with_user(self, app_key, user_id, permissions='r'):
        """
        Create new user_app relationship
        :param app_key:
        :param user_id:
        """
        with self.db.engine.connect() as connection:
            transaction = connection.begin()
            insert_user_app = insert(self.user_app).values(
                user_id=user_id,
                app_key=app_key,
                permissions=permissions
            )
            connection.execute(insert_user_app)
            transaction.commit()

    def add_new_user_app(self, name, user_id):
        """
        Create new application and make relation with user
        :param name:
        :type name: str
        :param user_id:
        :type user_id: int
        :return: created application
        :rtype: anarcho.core.services.apps.models.Application
        """
        app = self.create_app(str(uuid.uuid1()), name)
        self.link_app_with_user(app.app_key, user_id, 'w')

        return self.get_user_app(user_id, app.app_key)

    def get_app_by_key(self, app_key):
        """
        Find application with app_key
        :param app_key:
        :type app_key: str
        :return: application with app_key
        :rtype: anarcho.core.services.apps.models.Application
        """
        with self.db.engine.connect() as connection:
            select_query = select([self.apps]).where(self.apps.c.app_key == app_key)
            result = connection.execute(select_query).fetchone()
            return Application.from_row(result)

    def get_icon(self, app_key):
        # todo implement getting icon
        pass