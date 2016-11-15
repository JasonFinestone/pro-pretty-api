import os
import logging


basedir = os.path.abspath(os.path.dirname(__file__))
databasedir = os.path.join(basedir, 'databases')
logfiledir = os.path.join(basedir, 'logs')
logfile = os.path.join(logfiledir, 'pro-pretty-api.log')

## Application database for user details and app storage

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(databasedir, 'AppDb')
SQLALCHEMY_MIGRATE_REPO = os.path.join(databasedir, 'db_repository')

## Security
SECRET_KEY = "If you ate meat would you like the bone"

# Logging
# create a logging format
formatter = logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s')

logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)

# create a file handler
fileHandler = logging.handlers.RotatingFileHandler(logfile, maxBytes=(1048576*5), backupCount=7)
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formatter)

# create a console.logger to be run when developing
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)
