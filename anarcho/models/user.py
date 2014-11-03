import time
from anarcho import db
from flask.ext.login import UserMixin, make_secure_token
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(20))
    pass_hash = Column('pass_hash', String)
    email = Column('email', String(50), unique=True)
    registered_on = Column('registered_on', Integer)
    auth_token = Column('auth_token', String(50), )
    apps = relationship("Application", secondary="users_apps", backref="users")

    def __init__(self, email, name=None, password=None):
        self.email = email
        self.name = name
        if self.name is not None and password is not None:
            self.name = name
            self.hash_password(password)
            self.registered_on = time.time()
            self.update_auth_token()

    def update_auth_token(self):
        self.auth_token = make_secure_token(self.email, self.name)

    def hash_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_hash, password)

    def __repr__(self):
        return '<User %r>' % self.name
