#!/usr/bin/python3
"""Implement API endpoints for users"""
from flask import abort, make_response, request
from api.v1.views import app_views
import json
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'])
def get_users(user_id=None):
    """Retrieves the list of all User objects or a specific User by ID"""
    if user_id:
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        res_obj = user.to_dict()
    else:
        all_users = storage.all(User).values()
        users_list = []
        for user in all_users:
            users_list.append(user.to_dict())
        res_obj = users_list

    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object by ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    res_obj = {}
    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a new User object"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')

    new_user = User(**data)
    new_user.save()
    res_obj = new_user.to_dict()
    response = make_response(json.dumps(res_obj), 201)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User object by ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    # Update the User object with the new data
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at', 'password']:
            setattr(user, key, value)
    user.save()

    res_obj = user.to_dict()
    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
