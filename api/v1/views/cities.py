#!/usr/bin/python3
"""Implement API endpoints for cities"""
from flask import abort, make_response, request
from api.v1.views import app_views
import json
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'])
@app_views.route('/cities/<city_id>', methods=['GET'])
def get_cities(state_id=None, city_id=None):
    """Retrieves the list of all City objects or a specific City by ID"""
    if city_id:
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        res_obj = city.to_dict()
    elif state_id:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        cities_list = [city.to_dict() for city in state.cities]
        res_obj = cities_list
    else:
        all_cities = storage.all(City).values()
        cities_list = [city.to_dict() for city in all_cities]
        res_obj = cities_list

    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city object by ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    res_obj = {}
    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a new City object in a specified State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')

    new_city = City(**data)
    new_city.state_id = state.id
    new_city.save()
    res_obj = new_city.to_dict()
    response = make_response(json.dumps(res_obj), 201)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a City object by ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    # Update the City object with the new data
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    city.save()

    res_obj = city.to_dict()
    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
