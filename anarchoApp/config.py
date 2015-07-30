import os
from os.path import join

AUTO_RELOAD = False
DEBUG = False

anarcho_dir = os.path.dirname(__file__)

PID_FILE = join(anarcho_dir, 'anarcho.pid')

PORT = 5000
PORT_SECURE = 5443

# being used for making urls
# should looks like "world_visible_host.com"
HOST = '<PUT_CORRECT_HOST>'

PUBLIC_HOST = 'http://{0}{1}'.format(HOST, PORT)
PUBLIC_HOST_SECURE = 'https://{0}{1}'.format(HOST, PORT_SECURE)

SSL_PATH = {
    'crt': join(anarcho_dir, 'anarcho_server.crt'),
    'key': join(anarcho_dir, 'anarcho_server.key')
}

TMP_DIR = join(anarcho_dir, 'tmp')
LOGS_DIR = join(anarcho_dir, 'log')
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % join(anarcho_dir, 'anarcho.db')

# config for builds worker
STORAGE_WORKER = {
    # type currently allowed only local_storage
    'type': 'local_storage',
    # folder for storing build info
    'local_storage_dir': join(anarcho_dir, "builds"),
    # external hostname,
    # being used for making urls for static looks like
    # "http://world_visible_host.com"
    'local_storage_host': PUBLIC_HOST,
    'local_storage_host_https': PUBLIC_HOST_SECURE
}