#!/usr/bin/python3
""" """

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ close storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    """ """
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', 5000),
            threaded=True, debug=True)
