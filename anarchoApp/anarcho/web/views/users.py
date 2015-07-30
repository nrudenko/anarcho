from flask import Blueprint, request
from objects.injections import inject, KwArg
from werkzeug.exceptions import BadRequest

from anarcho.core.core_catalog import Services
from anarcho.core.services.users.exceptions import UserAlreadyExist, UserServiceException
from anarcho.extensions.api_login.manager import login_required
from anarcho.web.responses import TokenResponse, UserResponse, json_response
from anarcho.web.exceptions import AnarchoApiException

users_views = Blueprint('users', __name__, url_prefix='/api')


@users_views.route('/users', methods=['PUT'])
@inject(KwArg('_request', request))
@inject(KwArg('users_service', Services.users))
@inject(KwArg('tokens_service', Services.tokens))
def register(_request, users_service, tokens_service):
    request_params = _request.json
    if not request_params:
        raise BadRequest()

    name = request_params.get('name')
    email = request_params.get('email')
    password = request_params.get('password')
    try:
        users_service.create_user(email, password, name)
        token = tokens_service.create_token(email)
        return json_response(TokenResponse(token))
    except UserAlreadyExist as e:
        raise AnarchoApiException(e, 409)
    except UserServiceException as e:
        raise AnarchoApiException(e)


@users_views.route('/users/me', methods=['GET'])
@login_required
def me(user):
    return json_response(UserResponse(user))
