#!/usr/bin/python3
"""Defines api index"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def get_status():
    """Returns current status of api"""
    return {'status': 'OK'}
# Task3 ended here


@app_views.route('/stats')
def get_stats():
    """
    Retrieves the number of objs by type,and returns as JSON.
    """

    count = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User),
    }

    return (count)
