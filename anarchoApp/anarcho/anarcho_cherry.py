import os

import cherrypy
from anarcho import app


def run():
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': app.config['PORT'],
        'engine.autoreload.on': app.config['AUTO_RELOAD'],
        'log.screen': app.config['DEBUG'],
        'log.error_file': os.path.join(app.config['LOGS_DIR'], "error.log")
    })

    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app, '/')

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()