# the resource used for note taking
from flask_restful import Resource, reqparse, inputs
from models import User
from database import db_session
from datetime import datetime
from config import logger

class Register(Resource):
    # User registration
    def post(self):
            try:
                parser = reqparse.RequestParser()
                parser.add_argument('email', type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
                                    , required=True, help='A valid email is required', location='json')
                parser.add_argument('password', type=str, required=True, help='Password is required', location='json')
                parser.add_argument('first_name', type=str, required=True, help='First name is required'
                                    , location='json')
                parser.add_argument('last_name', type=str, required=True, help='Last name is required', location='json')

                args = parser.parse_args()
                #TODO: Add ip address and any standard info you can get from a browser like chrome

                _email = args['email']
                _password = args['password']
                _firstname = args['first_name']
                _lastname = args['last_name']
                _timestamp = datetime.today().strftime('%Y%m%d-%H:%M:%S')

                if _email is None or _password is None:
                    logger.critical("Required fields email or password are missing in request.")
                    return {'message': 'Unauthorized access'}, 403
                if User.query.filter_by(email=_email).first() is not None:
                    return {'message': 'Existing user'}, 400

                user = User(email=_email, first_name=_firstname, last_name=_lastname)
                user.hash_password(_password)
                db_session.add(user)
                db_session.commit()
                logger.info("New user created.")
                logger.debug("User created with email %s, first name %s, last name %s has been created.", user.email,
                             user.first_name, user.last_name)
                # Expect this to all go into a secure cookie on the client side
                return {'email': user.email}, 201

            except (SystemExit, KeyboardInterrupt):
                raise
            except Exception as e:
                logger.error(e, exc_info=True)


class Login(Resource):
    # Login with email and password or authorise with token
    def post(self):
            # The email field here is optional because token will be received in password field
            try:
                parser = reqparse.RequestParser()
                parser.add_argument('email', type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
                                    , required=False, help='Supplied email address must be valid.', location='json')
                parser.add_argument('password', type=str, required=True, help='Required information missing.', location='header')


                args = parser.parse_args()
                #TODO: Add ip address and any standard info you can get from a browser like chrome

                _email = args['email']
                _password = args['password']
                _timestamp = datetime.today().strftime('%Y%m%d-%H:%M:%S')

                if _email is None or _password is None:
                    logger.critical("Required fields email or password are missing in request.")
                    return {'message': 'Unauthorized access'}, 403
                if User.query.filter_by(email=_email).first() is not None:
                    return {'message': 'Existing user'}, 400

                user = User(email=_email, first_name=_firstname, last_name=_lastname)
                user.hash_password(_password)
                db_session.add(user)
                db_session.commit()
                logger.info("New user created.")
                logger.debug("User created with email %s, first name %s, last name %s has been created.", user.email,
                             user.first_name, user.last_name)
                return {'username': user.username}, 201

                pass
            except (SystemExit, KeyboardInterrupt):
                raise
            except Exception as e:
                logger.error(e, exc_info=True)
                return e

class Example(Resource):
    #
    def get(self):
        try:
            pass
        except Exception as e:
            return e

    # User registration
    def post(self):
            try:
                pass
            except (SystemExit, KeyboardInterrupt):
                raise
            except Exception as e:
                logger.error(e, exc_info=True)
                return e

    #
    def put(self):
            try:
                pass
            except Exception as e:
                logger.error(e, exc_info=True)
                return e

    #
    def delete(self):
        try:
            pass
        except Exception as e:
            logger.error(e, exc_info=True)
            return e
