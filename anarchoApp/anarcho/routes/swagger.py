from anarcho import app
from flask import jsonify
from flask_swagger import swagger


@app.route('/swagger/spec.json', methods=['GET'])
def spec():
    """
    Returns the swagger spec.
    Read more by this link https://github.com/swagger-api/swagger-spec/blob/master/versions/2.0.md
    :return:
    """
    swag = swagger(app)
    swag['info']['title'] = app.name
    swag['consumes'] = ['application/json']
    swag['produces'] = ['application/json']
    return jsonify(swag)
