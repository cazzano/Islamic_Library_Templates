from app import app as application
from flask import Flask

server = Flask(__name__)

# Expose the Dash app's server
server.wsgi_app = application.server

if __name__ == '__main__':
    application.run_server(debug=True)
