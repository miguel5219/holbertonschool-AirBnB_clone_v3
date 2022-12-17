#!/usr/bin/python3
""" new view for User object that handles all
default RESTFul API actions
"""

from models import storage
from api.v1.views import app_views
from models.user import User
from flask import jsonify, make_response
from flask import request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>')
def get_user(user_id=None):
    """ """
    if user_id is None:
        user_obj = [user.to_dict() for user in storage.all(User).values()]
        return make_response(jsonify(user_obj), 200)
    else:
        objs = storage.get(User, user_id)
        if objs is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            return make_response(jsonify(objs.to_dict()), 200)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id=None):
    objs = storage.get(User, user_id)
    if objs is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    storage.delete(objs)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    comp_data = request.get_json(silent=True, force=True)
    if comp_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        if 'email' not in comp_data:
            return make_response(jsonify({'error': 'Missing email'}), 400)
        if 'password' not in comp_data:
            return make_response(jsonify({'error': 'Missing password'}), 400)
        objs = User(**comp_data)
        objs.save()
        return make_response(jsonify(objs.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id=None):
    if user_id is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        objs = storage.get(User, user_id)
        if objs is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            comp_data = request.get_json(silent=True, force=True)
            if comp_data is None:
                return make_response(jsonify({'error': 'Not a JSON'}), 400)
            [setattr(objs, item, value) for item, value in comp_data.items()
             if item != ('id', 'email', 'created_at', 'updated_at')]
            objs.save()
            return make_response(jsonify(objs.to_dict()), 200)
