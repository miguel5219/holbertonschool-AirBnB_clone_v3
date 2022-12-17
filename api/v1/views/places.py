#!/usr/bin/python3
""" new view for Place objects that handles all
default RESTFul API actions
"""

from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from flask import Flask, jsonify, make_response
import requests
from flask import request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place(city_id=None):
    """ """
    objs = storage.get(City, city_id)
    if objs is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    objs_places = [place.to_dict() for place in storage.all(Place).values()
                   if place.city_id == city_id]
    return make_response(jsonify(objs_places), 200)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """ """
    objs = storage.get(Place, place_id)
    if objs is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        return make_response(jsonify(objs.to_dict()), 200)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """ """
    objs = storage.get(Place, place_id)
    if objs is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    storage.delete(objs)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id=None):
    """ """
    comp_data = request.get_json(silent=True, force=True)
    if comp_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        if 'name' not in comp_data:
            return make_response(jsonify({'error': 'Mising name'}), 400)
        if 'user_id' not in comp_data:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        obj = storage.get(City, city_id)
        objs_1 = storage.get(User, comp_data['user_id'])
        if obj is None or objs_1 is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        objs = Place(**comp_data)
        objs.city_id = city_id
        objs.save()
        return make_response(jsonify(objs.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id=None):
    """ """
    if place_id is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        objs = storage.get(Place, place_id)
        if objs is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            comp_data = request.get_json(silent=True, force=True)
            if comp_data is None:
                return make_response(jsonify({'error': 'Not a JSON'}), 400)
            [setattr(objs, key, value) for key, value in comp_data.items()
             if key != ('id', 'user_id', 'created_at', 'city_id', 'updated_at',
                        'state_id')]
            objs.save()
            return make_response(jsonify(objs.to_dict()), 200)
