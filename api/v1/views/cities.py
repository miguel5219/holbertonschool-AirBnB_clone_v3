#!/usr/bin/python3
""" create a new view for City objects that
handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def get_cities(state_id):
    """ """
    comp = storage.get(State, state_id)
    if comp is not None:
        cities_ = []
        for city in storage.all(City).values():
            if city.state_id == state_id:
                cities_.append(city.to_dict())
        return jsonify(cities_), 200

    return abort(404, "Not found")


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def cities_by_id(city_id):
    """ """
    for city_ in storage.all(City).values():
        if city_.id == city_id:
            return jsonify(city_.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def del_cities(city_id):
    """ """
    city_ = storage.get(City, city_id)
    if not city_:
        abort(404)
    city_.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def cities_posts(state_id):
    """ """
    obj = request.get_json()
    state = storage.get(State, state_id)
    if obj is None:
        abort(400, "Not a JSON")

    if state is None:
        abort(404, "Not found")

    if 'name' not in obj:
        abort(400, "Missing name")

    city_new = City(**obj)
    setattr(city_new, 'state_id', state_id)
    city_new.save()
    return jsonify(city_new.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def put_cities(city_id):
    """ update state """
    city_ = storage.get(City, city_id)
    comp = request.get_json()
    if city_ is None:
        abort(404)

    if comp is None:
        abort(400, "Not a JSON")

    for k, value in comp.items():
        if k in ["id", "state_id", "created_at", "updated_at"]:
            continue
        else:
            setattr(city_, k, value)
    city_.save()
    return jsonify(city_.to_dict()), 200
