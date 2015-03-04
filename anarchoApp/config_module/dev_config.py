import os
from os.path import join

anarcho_dir = os.path.dirname(__file__)

PORT = 5000
PORT_SECURE = 5443

HOST = 'localhost'

PUBLIC_HOST = 'http://{0}:{1}'.format(HOST, PORT)
PUBLIC_HOST_SECURE = 'https://{0}:{1}'.format(HOST, PORT_SECURE)

SSL_PATH = {
    'crt': join(anarcho_dir, 'anarcho_server.cer'),
    'key': join(anarcho_dir, 'anarcho_server.key')
}

TMP_DIR = join(anarcho_dir, 'tmp')
LOGS_DIR = join(anarcho_dir, 'log')
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % join(anarcho_dir, 'anarcho.db')

AUTO_RELOAD = True
DEBUG = True

STORAGE_WORKER = {
    'type': 'local_storage',
    'local_storage_dir': join(anarcho_dir, "builds"),
    'local_storage_host': PUBLIC_HOST,
    'local_storage_host_https': PUBLIC_HOST_SECURE
}