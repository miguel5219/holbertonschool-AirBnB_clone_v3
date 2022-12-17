#!/usr/bin/python3
""" new view for Review object that handles all
default RESTFul API actions
"""

from models import storage
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, make_response
from flask import request
import requests


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id=None):
    objs = storage.get(Place, place_id)
    if objs is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    objs_reviews = [review.to_dict() for review in storage.all(Review).values()
                    if review.place_id == place_id]
    return make_response(jsonify(objs_reviews), 200)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id=None):
    objs = storage.get(Review, review_id)
    if objs is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        return make_response(jsonify(objs.to_dict()), 200)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    objs =storage.get(Review, review_id)
    if objs is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    storage.delete(objs)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id=None):
    comp_data = request.get_json(silent=True, force=True)
    if comp_data is None:
        return make_response(jsonify({'error': 'Not JSON'}), 400)
    else:
        if 'text' not in comp_data:
            return make_response(jsonify({'error': 'Missing text'}), 400)
        if 'user_id' not in comp_data:
            return make_response(jsonify({'error':'Missing user_id'}), 400)
    objs = storage.get(Place, place_id)
    objs_1 = storage.get(User, comp_data['user_id'])
    if objs is None or objs_1 is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        N_review = Review(**comp_data)
        N_review.place_id = place_id
        N_review.save()
    return make_response(jsonify(N_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_reviews(review_id=None):
    if review_id is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        objs = storage.get(Review, review_id)
        if objs is None:
            return make_response(jsonify({'error':'Not found'}), 404)
        else:
            comp_data = request.get_json(silent=True, force=True)
            if comp_data is None:
                return make_response(jsonify({'error': 'Not a JSON'}), 400)
            [setattr(objs, key, value) for key, value in comp_data.items()
             if key != ('id', 'user_id', 'created_at', 'place_id', 'updated_id', 'state_id')]
            objs.save()
            return make_response(jsonify(objs.to_dict()), 200)
