import time
from sqlalchemy import Column, Integer, String

from anarcho import db
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    pass_hash = Column(String)
    email = Column(String(50), unique=True)
    registered_on = Column(Integer)

    apps = relationship("Application", secondary="users_apps", backref="users")
    token = relationship("Token", uselist=False, backref="users")

    def __init__(self, email=None, name=None, password=None):
        self.email = email
        self.name = name
        if self.name is not None and password is not None:
            self.name = name
            self.hash_password(password)
            self.registered_on = time.time()

    def hash_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_hash, password)

    def __repr__(self):
        return '<User %r>' % self.name
