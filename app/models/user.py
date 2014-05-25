from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column('user_id', Integer, primary_key=True)
    username = Column('username', String(20), unique=True, index=True)
    password = Column('password', String(10))
    email = Column('email', String(50), unique=True, index=True)
    registered_on = Column('registered_on', DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)