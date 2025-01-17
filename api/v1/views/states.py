#!/usr/bin/python3
""" Create a new VIEW for State objects that
handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False, methods=['GET'])
def get_states():
    """ use to_dict() to retrieve an object into a valid JSON """
    list_ = []
    for state in storage.all(State).values():
        list_.append(state.to_dict())
    return jsonify(list_)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def states_by_id(state_id):
    """ Retrieves a State object: GET /api/v1/states/<state_id> """
    for state in storage.all(State).values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_states(state_id):
    """ Deletes a State object:: DELETE /api/v1/states/<state_id> """
    state = storage.get(State, state_id)
    if state is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def state_post():
    """ Creates a State: POST /api/v1/states.
    You must use request.get_json from Flask to
    transform the HTTP body request to a dictionary
    """
    if not request.get_json():
        abort(400, "Not a JSON")

    if 'name' not in request.get_json().keys():
        abort(400, "Missing name")

    state_new = State(**request.get_json())
    state_new.save()
    return jsonify(state_new.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def states_put(state_id):
    """Updates a State object: PUT /api/v1/states/<state_id>. """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    for key, value in request.get_json().items():
        if key in ["id", "created_at", "updated_at"]:
            continue
        else:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200
