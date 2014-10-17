#!flask/bin/python
from app.models.user import User
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
    user = User(email, username, password)
    db.session.add(user)
    db.session.commit()

    application = Application("TestApp")
    user_app = UserApp(user.email, application.app_key, "w")

    build = Build(application.app_key, "11", "1.1", "release notes")
    db.session.add(application)
    db.session.add(user_app)
    db.session.add(build)

    db.session.commit()


@manager.command
def drop_session(name):
    user = User.query.filter_by(username=name).first()
    print 'Old token ', user.auth_token
    user.update_auth_token()
    print 'New token ', user.auth_token
    db.session.commit()


if __name__ == "__main__":
    manager.run()
