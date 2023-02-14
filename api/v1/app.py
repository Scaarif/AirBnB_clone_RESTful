#!/usr/bin/python3
""" Instantiates a Flask application & registers BluePrints """
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
import os


# instantiate a Flask application
app = Flask(__name__)
# register app_views Blueprint (include url_prefix)
app.register_blueprint(app_views, url_prefix='/api/v1/')


@app.teardown_appcontext
def close_context(self):
    """ tears down current session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Creates a handler for 404 errors that returns a JSON-formatted
    404 status code response """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', 5000), threaded=True)
