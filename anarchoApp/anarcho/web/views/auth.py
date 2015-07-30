from flask import request, Blueprint
from objects.injections import inject, KwArg
from werkzeug.exceptions import BadRequest

from anarcho.core.core_catalog import Services
from anarcho.core.services.users.exceptions import WrongCredentials
from anarcho.web.responses import TokenResponse, json_response
from anarcho.web.exceptions import AnarchoApiException

auth_views = Blueprint('auth', __name__, url_prefix='/api')


@auth_views.route('/authorize', methods=['POST'])
@inject(KwArg('_request', request))
@inject(KwArg('users_service', Services.users))
@inject(KwArg('tokens_service', Services.tokens))
def authorize(_request, users_service, tokens_service):
    """
    Perform authorization

    """
    request_params = _request.json
    if request_params is None:
        raise BadRequest()

    email = request_params.get('email')
    password = request_params.get('password')
    try:
        users_service.assert_credentials(email, password)
        token = tokens_service.get_token_by_auth_id(email)
        if not token:
            token = tokens_service.create_token(email)
        return json_response(TokenResponse(token))
    except WrongCredentials as e:
        raise AnarchoApiException(e, status_code=401)
