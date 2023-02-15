#!/usr/bin/python3
""" Defines a view for Place objects: handles all default RESTful API
    actions (i.e. GET, PUT, POST & DELETE) """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places')
def city_places(city_id):
    """ retrieves all the Place objects of a City """
    # get the city, and if None, raise a 404
    city = storage.get(City, city_id)
    if city:
        return jsonify([place.to_dict() for place in city.places])
    abort(404)  # city is None


@app_views.route('/places/<place_id>')
def place(place_id):
    """ retrieves Place object (of ID), raising a 404 error if
    not found """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ deletes a Place object, returning an empty dict with status 200
    if object (of id) is found, else raises a 404 error """
    # get the object with id then delete it
    obj = storage.get(Place, place_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    abort(404)  # obj is None


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def add_place(city_id):
    """ creates a new Place object
    Returns the new place and status code 201 """
    # check that the request body is JSON
    if not request.json:
        return jsonify('Not a JSON'), 400
    # check that city exists, else a 404 error
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    place_info = request.get_json()  # returns a dict
    checks = ['user_id', 'name']
    for check in checks:
        if check not in place_info:
            abort(make_response(jsonify('Missing {}'.format(check)), 400))
    # check that user (user_id) is valid
    user = storage.get(User, place_info['user_id'])
    if not user:
        abort(404)
    # create new Place
    place_info.update({'city_id': city_id})
    place = Place(**place_info)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """ updates a Place object
    Returns the updated place + status code 200 if successful,
    raising 4XX errors  otherwise """
    # get the place to update
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        # abort(400)  # Not a JSON
        return jsonify('Not a JSON'), 400
    place_info = request.get_json()
    # update place (by updating/adding its attributes)
    ignore = ['id', 'created_at', 'updated_at', 'city_id', 'user_id']
    for key, value in place_info.items():
        if key not in ignore:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
