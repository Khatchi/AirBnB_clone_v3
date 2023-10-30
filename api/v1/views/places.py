#!/usr/bin/python3
"""Implement api obj: states"""
from flask import abort, make_response, request
from api.v1.views import app_views
import json
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'])
@app_views.route('/places/<place_id>', methods=['GET'])
def get_places(city_id=None, place_id=None):
    """Retrieves the list of all Place objects of a City,
    or a specific Place by ID
    """
    if place_id:
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        res_obj = place.to_dict()
    else:
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        places_list = []
        for place in city.places:
            places_list.append(place.to_dict())
        res_obj = places_list

    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    res_obj = {}
    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a new Place object in a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    new_place = Place(**data)
    new_place.city_id = city.id
    new_place.save()
    res_obj = new_place.to_dict()
    response = make_response(json.dumps(res_obj), 201)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    # Update the Place object with the new data
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()

    res_obj = place.to_dict()
    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
