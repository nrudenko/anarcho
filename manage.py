#!flask/bin/python
from flask.ext.script import Manager

from app import app, db

manager = Manager(app)


@manager.command
def run_dev():
    """
    Run app for development
    """
    import config_module

    manager.app.config.from_object(config_module.DevConfig)
    manager.app.run(debug=True,
                    use_debugger=True,
                    use_reloader=True)


@manager.command
def init_db():
    """
    Init db (creates all tables)
    """
    db.create_all()


@manager.command
def init_db_stub():
    """
    Init db and add stub values
    """
    from app.models.user import User, UserApp
    from app.models.application import Application
    from app.models.build import Build

    init_db()

    username = "admin"
    password = "admin"
    email = "admin@mail.com"
    user = User(username, password, email)
    db.session.add(user)
    db.session.commit()

    application = Application("TestApp")
    user_app = UserApp(user.id, application.app_key)

    build = Build(application.app_key, "11", "1.1", "release notes")
    db.session.add(application)
    db.session.add(user_app)
    db.session.add(build)

    db.session.commit()


if __name__ == "__main__":
    manager.run()
