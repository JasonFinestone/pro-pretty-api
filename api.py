from flask import Flask
from flask_restful import Api
from flask.ext.login import LoginManager, login_required
from werkzeug.security import gen_salt
from flask_oauthlib.provider import OAuth2Provider

from flask.ext.login import current_user, UserMixin

app = Flask(__name__)
oauth = OAuth2Provider(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"

# restful api
api = Api(app, decorators=[oauth.require_oauth('email'), login_required()])

from resources import auth_resource

api.add_resource(auth_resource.Register, '/register', endpoint='register')

#from database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    auth_resource.db_session.remove()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

'''
if __name__ == '__main__':
    app.run(debug=True)
'''


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'