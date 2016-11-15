from api import app
from os import environ
from config import logger


def run_server():
    port = int(environ.get('PORT', 5000))
    logger.info(" * Starting Pro-Pretty API")
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=True)

if __name__ == "__main__":
    run_server()
