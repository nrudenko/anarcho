from flask import request, g

from anarcho import app
from anarcho.access_manager import login_required
from anarcho.models.user import User
from anarcho.serializer import serialize
from anarcho.reasons import errors
from anarcho.helpers.response import Response


@app.route('/api/register', methods=['POST'])
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
                    error: user_already_registered
        403:
            description: Different errors
            schema:
                type: object
                required:
                - error
                properties:
                    error:
                        type: string
            examples:
                application/json:
                    - error: invalid_user_name
                    - error: user_name_is_empty
                    - error: invalid_user_name_length
                    - error: invalid_email
                    - error: email_is_empty
                    - error: invalid_email_format
                    - error: invalid_email_length
                    - error: invalid_password
                    - error: empty_password
                    - error: invalid_password_length
    """
    if 'name' in request.json:
        name = request.json['name']
    else:
        return Response.failure(errors.INVALID_USER_NAME)

    if 'email' in request.json:
        email = request.json['email'].lower()
    else:
        return Response.failure(errors.INVALID_EMAIL)

    if 'password' in request.json:
        password = request.json['password']
    else:
        return Response.failure(errors.INVALID_PASSWORD)

    try:
        result = User.register(name, email, password)
    except ValueError as exc:
        return Response.failure(exc.args)

    return serialize(result)


@app.route('/api/login', methods=['POST'])
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
        403:
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
                    error: wrong_credentials
    """
    email = request.json['email'].lower()
    password = request.json['password']
    u = User.query.filter(User.email == email).first()
    if u is not None:
        if u.verify_password(password):
            return serialize(u.token)

    return Response.failure(errors.WRONG_CREDENTIALS)


@app.route('/api/user', methods=['GET'])
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
                    error: unauthorized
    """
    return serialize(g.user)
