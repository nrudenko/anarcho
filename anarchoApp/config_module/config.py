import os
from os.path import join

anarcho_dir = os.path.dirname(__file__)

# being used for making upload url for plugin config looks like
# "http://world_visible_host.com"
PUBLIC_HOST = '<PUT_CORRECT_HOST>'
PORT = 8080
TMP_DIR = join(anarcho_dir, 'tmp')
LOGS_DIR = join(anarcho_dir, 'log')
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % join(anarcho_dir, 'anarcho.db')

# config for builds worker
STORAGE_WORKER = {
    # type currently allowed only local_storage
    'type': 'local_storage',
    # folder for storing build info
    'storage_dir': join(anarcho_dir, "builds"),
    # external hostname,
    # being used for making urls for static looks like
    # "http://world_visible_host.com"
    'storage_host_name': '<PUT_CORRECT_STORAGE_HOST>'
}