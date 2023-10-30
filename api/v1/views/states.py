#!/usr/bin/python3
"""Implement api obj: states"""
from flask import abort, make_response, request
from api.v1.views import app_views
import json
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'])
def get_states(state_id=None):
    """Retrieves the list of all State objects or a specific State by ID"""
    if state_id:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        res_obj = state.to_dict()
    else:
        all_states = storage.all(State).values()
        states_list = []
        for state in all_states:
            states_list.append(state.to_dict())
        res_obj = states_list

    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/state/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a state obj by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    res_obj = {}
    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return (response)


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a new State object"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')

    new_state = State(**data)
    new_state.save()
    res_obj = new_state.to_dict()
    response = make_response(json.dumps(res_obj), 201)
    response.headers['Content-Type'] = 'application/json'
    return (response)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a State object by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    # Update the State object with the new data
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()

    res_obj = state.to_dict()
    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return (response)
