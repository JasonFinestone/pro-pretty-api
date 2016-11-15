from flask import Flask
from flask_restful import Api

app = Flask(__name__)
# restful api
api = Api(app)

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