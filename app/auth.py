from app import login_manager
from app.models.user import User
from flask import g, Response


@login_manager.unauthorized_handler
def unauthorized():
    return Response('{"error":"unauthorized"}', 401, {'WWWAuthenticate': 'Basic realm="Login Required"'})


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@login_manager.request_loader
def load_user_from_request(request):
    auth_token = request.headers.get('x-auth-token')
    user = None
    if auth_token:
        user = User.query.filter_by(auth_token=auth_token).first()
        g.user = user
    return user

