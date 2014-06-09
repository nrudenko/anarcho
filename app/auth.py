from app import login_manager, app, db
from app.models.user import User
from flask import session, g, request, render_template, url_for, redirect, Response
from flask.ext.login import login_user, logout_user, make_secure_token


@login_manager.unauthorized_handler
def unauthorized():
    return "{unauthorized}"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    return None


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = load_user(session['user_id'])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    api_key = make_secure_token(email, username, password)
    user = User(username, password, email, api_key)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        print g.user
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        return redirect(url_for('login'))
    login_user(registered_user)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

