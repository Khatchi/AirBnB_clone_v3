#!/usr/bin/python3
"""Implement API endpoints for amenities"""
from flask import abort, make_response, request
from api.v1.views import app_views
import json
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'])
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenities(amenity_id=None):
    """Retrieves the list of all Amenity objects or a specific Amenity by ID"""
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        res_obj = amenity.to_dict()
    else:
        all_amenities = storage.all(Amenity).values()
        amenities_list = [amenity.to_dict() for amenity in all_amenities]
        res_obj = amenities_list

    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    res_obj = {}
    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates a new Amenity object"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')

    new_amenity = Amenity(**data)
    new_amenity.save()
    res_obj = new_amenity.to_dict()
    response = make_response(json.dumps(res_obj), 201)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    # Update the Amenity object with the new data
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()

    res_obj = amenity.to_dict()
    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
