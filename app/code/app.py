import os
from project import create_app

API_KEY = os.environ['API_KEY']


# Calls the application factory function to construct a Flask application
app = create_app()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

