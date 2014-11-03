from flask.ext.script import Manager

from anarcho import app, db

manager = Manager(app)


@manager.command
def start_dev():
    """
    Run app for development
    """
    from anarcho import anarcho_cherry
    import config_module

    manager.app.config.from_object(config_module.DevConfig)
    anarcho_cherry.prepare_dev_server()
    anarcho_cherry.run()


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
    from anarcho.models.user import User
    from anarcho.models.user_app import UserApp
    from anarcho.models.application import Application
    from anarcho.models.build import Build

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
def drop_session(email):
    from anarcho.models.user import User

    user = User.query.filter_by(email=email).first()
    print 'Old token ', user.auth_token
    user.update_auth_token()
    print 'New token ', user.auth_token
    db.session.commit()


@manager.command
def start():
    from anarcho import anarcho_cherry
    print "Anarcho starting..."
    anarcho_cherry.prepare_prod_server()
    anarcho_cherry.run()

@manager.command
def stop():
    import os
    import signal

    pid_file = open('anarcho.pid')
    pid = pid_file.readline()
    pid_file.close()
    os.kill(int(pid), signal.SIGQUIT)
    print "Anarcho stopped..."


@manager.command
def restart():
    stop()
    start()


def main():
    manager.run()
