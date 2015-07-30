from flask import jsonify
from flask.blueprints import Blueprint
from flask.ext.swagger import swagger
from flask.globals import current_app

general = Blueprint('general', __name__, url_prefix='', static_folder='../static/', static_url_path='')


@general.route('/', methods=['GET'])
def index():
    return general.send_static_file("index.html")


@general.route('/certs', methods=['GET'])
def cert():
    return general.send_file(general.config['SSL_PATH']['crt'],
                             mimetype='application/x-x509-server-cert',
                             as_attachment=True)


@general.route('/swagger/spec.json', methods=['GET'])
def spec():
    """
    Returns the swagger spec.
    Read more by this link https://github.com/swagger-api/swagger-spec/blob/master/versions/2.0.md
    :return:
    """
    swag = swagger(current_app)
    swag['info']['title'] = current_app.name
    swag['consumes'] = ['application/json']
    swag['produces'] = ['application/json']
    return jsonify(swag)

    # @general.route('ping', methods=['GET'])
    # def ping():
    #     return 'ping'

    # @app.errorhandler(404)
    # @app.errorhandler(405)
    # def stub(e):
    #     return redirect("/404.html")


    # @app_permissions(permissions=['w', 'r'])
    #     def get_plugin_config(user, app_key):
    # user_app = UserApp.query.filter_by(app_key=app_key, permission='u').first()
    # if user_app is None:
    #     return make_response('{"error":"app_not_found"}', 404)
    # user = user_app.user
    # response = {
    #     'host': app.config['PUBLIC_HOST'],
    #     'app_key': app_key,
    #     'api_token': user.token.auth_token
    # }
    # return jsonify(response)
