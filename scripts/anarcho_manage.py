"""

Usage:
    anarcho init [<CONFIG_FILE>]
    anarcho (start | stop | restart | init_db | stub_db)

Options:
    -c CONFIG_FILE --config=CONFIG_FILE  Path to config for init

"""
import shutil
from os.path import expanduser
import os

from docopt import docopt


def try_backup_existing_config(config_path):
    try:
        config_dst_bkp = config_path + ".bkp"
        shutil.copy(config_path, config_dst_bkp)
    except OSError:
        pass
    except IOError:
        pass


def init_config(config_src):
    config_path = os.path.join(expanduser("~"), ".anarcho", "config.py")
    config_dst = config_path
    if config_src is None:
        import config_module

        config_src = os.path.join(os.path.dirname(config_module.__file__), "config.py")

    try_backup_existing_config(config_dst)

    try:
        os.makedirs(os.path.dirname(config_dst))
    except OSError:
        pass
    shutil.copy(config_src, config_dst)

    print 'Created config: %s' % config_path


def init(config_file=None):
    """
    Init app
    """
    init_config(config_file)


def init_db():
    from anarcho import db

    db.create_all()


def stub_db():
    """
    Init db and add stub values
    """
    from anarcho import db

    from anarcho.models.user import User
    from anarcho.models.user_app import UserApp
    from anarcho.models.application import Application
    from anarcho.models.build import Build

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


def drop_session(email):
    from anarcho import db
    from anarcho.models.user import User

    user = User.query.filter_by(email=email).first()
    print 'Old token ', user.auth_token
    user.update_auth_token()
    print 'New token ', user.auth_token
    db.session.commit()


def start():
    from anarcho import anarcho_cherry

    print "Anarcho starting..."
    anarcho_cherry.run()


def stop():
    import os
    import signal

    pid_file_path = 'anarcho.pid'
    if os.path.exists(pid_file_path):
        pid_file = open(pid_file_path)
        pid = pid_file.readline()
        pid_file.close()
        os.kill(int(pid), signal.SIGQUIT)
    print "Anarcho stopped..."


def restart():
    stop()
    start()


def main():
    args = docopt(__doc__)
    if args['stub_db']:
        stub_db()
    if args['init']:
        init(args['<CONFIG_FILE>'])
        pass
    if args['start']:
        start()
        pass
    if args['stop']:
        stop()
        pass
    if args['restart']:
        stop()
        pass
    if args['init_db']:
        init_db()
        pass