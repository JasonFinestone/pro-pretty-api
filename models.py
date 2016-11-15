from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean, DateTime, func, Text
from sqlalchemy.orm import relationship, backref
from database import Base, db_session
from passlib.apps import custom_app_context as pwd_context
from flask.ext.login import current_user, UserMixin


class Parent(Base):
    __abstract__ = True
    created_at = Column(DateTime, default=func.current_timestamp())
    modified_at = Column(DateTime, default=func.current_timestamp(),
                            onupdate=func.current_timestamp())


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    # Why 45 characters for IP Address ?
    # See http://stackoverflow.com/questions/166132/maximum-length-of-the-textual-representation-of-an-ipv6-address/166157#166157
    last_login_ip = Column(String(45))
    current_login_ip = Column(String(45))
    login_count = Column(Integer)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return '<User %r>' % self.email

class Client(Base):
    client_id = Column(String(40), primary_key=True)
    client_secret = Column(String(55), nullable=False)

    user_id = Column(ForeignKey('user.id'))
    user = relationship('User')

    _redirect_uris = Column(Text)
    _default_scopes = Column(Text)

    @property
    def client_type(self):
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []

class Grant(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User')
    client_id = Column(String(40), ForeignKey('client.client_id'), nullable=False,)
    client = relationship('Client')
    code = Column(String(255), index=True, nullable=False)
    redirect_uri = Column(String(255))
    expires = Column(DateTime)
    _scopes = Column(Text)

    def delete(self):
        db_session.delete(self)
        db_session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(Base):
    id = Column(Integer, primary_key=True)
    client_id = Column(String(40), ForeignKey('client.client_id'), nullable=False,)
    client = relationship('Client')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')
    # currently only bearer is supported
    token_type = Column(String(40))
    access_token = Column(String(255), unique=True)
    refresh_token = Column(String(255), unique=True)
    expires = Column(DateTime)
    _scopes = Column(Text)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []
