import os

import cherrypy
from cherrypy._cpserver import Server
from anarcho import app


def run():
    config = {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': app.config['PORT'],
        'engine.autoreload.on': app.config['AUTO_RELOAD'],
        'log.screen': app.config['DEBUG'],
        'log.error_file': os.path.join(app.config['LOGS_DIR'], 'error.log')
    }
    cherrypy.config.update(config)

    cherrypy.tree.graft(app, '/')

    https_server = Server()
    https_server.socket_host = '0.0.0.0'
    https_server.socket_port = app.config['PORT_SECURE']
    https_server.ssl_module = 'pyopenssl'
    https_server.ssl_certificate = app.config['SSL_PATH']['crt']
    https_server.ssl_private_key = app.config['SSL_PATH']['key']

    https_server.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()