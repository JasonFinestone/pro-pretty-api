from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship, backref
from database import Base
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import gen_salt
from config import SECRET_KEY


class Parent(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    modified_at = Column(DateTime, default=func.current_timestamp(),
                            onupdate=func.current_timestamp())


roles_users = Table('roles_users',
                       Column('user_id', Integer(),
                                 ForeignKey('auth_user.id')),
                       Column('role_id', Integer(),
                                 ForeignKey('auth_role.id')))


class Role(Base):
    __tablename__ = 'auth_role'
    name = Column(String(80), nullable=False, unique=True)
    description = Column(String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role %r>' % self.name


class User(Base):
    __tablename__ = 'auth_user'
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
    roles = relationship('Role', secondary=roles_users, backref=backref('users', lazy='dynamic'))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User %r>' % self.email
