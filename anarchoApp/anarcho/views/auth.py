from anarcho import db
from anarcho.access_manager import login_required
from anarcho.serializer import serialize
from anarcho.services.exceptions import UserServiceException, UserNotAuthorized, UserAlreadyExist
from anarcho.services.user_service import UserService
from anarcho.view_utils import AnarchoApiException
from flask import request, g, Blueprint
from werkzeug.exceptions import BadRequest

auth = Blueprint("auth", __name__, url_prefix="/api")


@auth.route('/user', methods=['PUT'])
def register():
    """
    Register user
    ---
    tags:
        - auth
    parameters:
        - name: name
          in: formData
          type: string
          required: true
        - name: email
          in: formData
          type: string
          required: true
        - name: password
          in: formData
          type: string
          required: true
    responses:
        200:
            description: User registered successfully
            schema:
                type: object
                required:
                - authToken
                properties:
                    authToken:
                        type: string
            examples:
                application/json:
                    authToken: d8058758acbddce3cfa4308bbfe8a7b9
        409:
            description: User already registered
            schema:
                type: object
                required:
                - error
                properties:
                    error:
                        type: string
            examples:
                application/json:
                    - error:user_already_exist
        400:
            description: Data validation errors
            schema:
                type: object
                required:
                - error
                properties:
                    error:
                        type: string
            examples:
                application/json:
                    - error:username_length_is_wrong
                    - error:email_format_is_wrong
                    - error:password_is_empty
                    - error:password_is_too_short
    """
    request_params = request.json
    if not request_params:
        raise BadRequest()

    name = request_params.get('name')
    email = request_params.get('email')
    password = request_params.get('password')
    try:
        user_service = UserService(db)
        user_service.create_user(name, email, password)
        token = user_service.authenticate(email, password)
        return serialize(token)
    except UserAlreadyExist as e:
        raise AnarchoApiException(e, 409)
    except UserServiceException as e:
        raise AnarchoApiException(e)


@auth.route('/user', methods=['POST'])
def login():
    """
    User login
    ---
    tags:
        - auth
    parameters:
        - name: email
          in: formData
          type: string
          required: true
        - name: password
          in: formData
          type: string
          required: true
    responses:
        200:
            description: Login successful
            schema:
                type: object
                required:
                - email
                - password
                properties:
                    email:
                        type: string
                    password:
                        type: string
            examples:
                application/json:
                    authToken: 5addfaee6d90df1a979119dd34332597
        401:
            description: Wrong credentials
            schema:
                type: object
                required:
                - error
                properties:
                    error:
                        type: string
            examples:
                application/json:
                    error: user_not_authorized
    """
    request_params = request.json
    if request_params is None:
        raise BadRequest()

    email = request_params.get('email')
    password = request_params.get('password')
    try:
        token = UserService(db).authenticate(email, password)
        return serialize(token)
    except UserNotAuthorized as e:
        raise AnarchoApiException(e, 401)


@auth.route('/user', methods=['GET'])
@login_required
def user():
    """
    Get user info
    ---
    tags:
        - auth
    parameters:
        - name: x-auth-token
          in: header
          type: string
          required: true
          default: d8058758acbddce3cfa4308bbfe8a7b9
    responses:
        200:
            description: User info
            schema:
                type: object
                required:
                - id
                - name
                properties:
                    id:
                        type: int
                    name:
                        type: string
            examples:
                application/json:
                    id: 1
                    name: boonya
        401:
            description: Unauthorized user
            schema:
                type: object
                required:
                - error
                properties:
                    error:
                        type: string
            examples:
                application/json:
                    error: user_not_authorized
    """
    return serialize(g.user)
