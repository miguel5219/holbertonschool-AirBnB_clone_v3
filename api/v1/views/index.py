#!/usr/bin/ppython3
""" """

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.state import State
from models.review import Review

classes ={
    "cities": City, "amenities": Amenity,
    "places": Place, "users": User,
    "states": State, "reviews": Review
}

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_route():
    """ """
    return jsonify({'status': 'OK'})

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def stats():
    count_objects = {}
    for key, value in classes.items():
        count_objects[key] = storage.count(value)
    return jsonify(count_objects)
