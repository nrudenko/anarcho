from anarcho import app
from flask import redirect, Response, send_file

@app.route('/')
def index():
    return app.send_static_file("index.html")


@app.route('/api/cert', methods=['GET'])
def cert():
    return send_file(app.config['SSL_PATH']['crt'],
                     mimetype='application/x-x509-server-cert',
                     as_attachment=True)


@app.route('/api/ping', methods=['GET'])
def ping():
    return Response(__version__(), status=200)


@app.errorhandler(404)
@app.errorhandler(405)
def stub(e):
    return redirect("/404.html")