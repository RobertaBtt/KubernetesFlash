from flask import Flask
import os
from .routes import main
# API_KEY = os.environ['API_KEY']

# ----------------------------
# Creation of the app
# ----------------------------


def create_app():
    # Create the Flask application
    app = Flask(__name__)
    app.register_blueprint(main)
    return app

