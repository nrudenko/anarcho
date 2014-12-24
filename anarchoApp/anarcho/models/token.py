import time
from sqlalchemy import Column, Integer, String, ForeignKey
import uuid

from anarcho.access_manager import make_secure_token
from sqlalchemy.orm import relationship
from anarcho import db


class Token(db.Model):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    auth_token = Column(String(50))
    registered_on = Column(Integer)
    user = relationship("User", uselist=False, backref="tokens")

    def __init__(self, user):
        self.user_id = user.id
        self.auth_token = make_secure_token(str(uuid.uuid4()))
        self.registered_on = time.time()