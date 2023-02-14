#!/usr/bin/python3
""" Define app_views' routes? """
from api.v1.views import app_views
from flask import jsonify


# first route /status on the object app_views
@app_views.route('/status')
def status():
    """ Returns a JSON "status": "OK" """
    return jsonify({'status': 'OK'})
