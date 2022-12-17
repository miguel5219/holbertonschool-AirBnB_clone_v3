#!/usr/bin/python3
""" new view for Amenity objects that handles all default
RESTFul API actions
"""

from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from flask import jsonify, make_response
from flask import request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>')
def get_amenities(amenity_id=None):
    """ """
    if amenity_id is None:
        objs_amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
        return make_response(jsonify(objs_amenities), 200)
    else:
        objs = storage.get(Amenity, amenity_id)
        if objs is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            return make_response(jsonify(objs.to_dict()), 200)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id=None):
    objs = storage.get(Amenity, amenity_id)
    if objs is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    storage.delete(objs)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    data_comp = request.get_json(silent=True, force=True)
    if data_comp is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        if 'name' not in data_comp:
            return make_response(jsonify({'error': 'Missing name'}), 400)

    objs = Amenity(**data_comp)
    objs.save()
    return make_response(jsonify(objs.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenities(amenity_id=None):
    if amenity_id is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        objs = storage.get(Amenity, amenity_id)
        if objs is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        else:
            data_comp = request.get_json(silent=True, force=True)
            if data_comp is None:
                return make_response(jsonify({'error': 'Not a JSON'}), 400)
            [setattr(objs, item, value) for item, value in data_comp.items()
             if item != ('id', 'created_at', 'updated_at')]
            objs.save()
            return make_response(jsonify(objs.to_dict()), 200)
