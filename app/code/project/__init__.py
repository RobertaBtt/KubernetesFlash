from flask import Flask
from .routes import main


# ----------------------------
# Creation of the app
# ----------------------------
def create_app():
    # Create the Flask application
    app = Flask(__name__)
    app.register_blueprint(main)
    return app
