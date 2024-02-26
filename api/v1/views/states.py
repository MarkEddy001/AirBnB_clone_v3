#!/usr/bin/python3
"""states"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from datetime import datetime
import uuid


@app_views.route('/states/', methods=['GET'])
def list_states():
    """Retrieves a list of all State objects"""
    list_states = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a State object"""
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    return jsonify(state_obj[0])


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    state_obj.remove(state_obj[0])
    for obj in all_states:
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a new State"""
    # Check if the request body is valid JSON
    if not request.is_json:
        abort(400, description='Not a JSON')

    # Get the JSON data from the request body
    data = request.get_json()

    # Check if the dictionary contains the key 'name'
    if 'name' not in data:
        abort(400, description='Missing name')

    # Create a new State object
    new_state = State(**data)
    storage.new(new_state)
    storage.save()

    # Return the new State with status code 201
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)

    # Check if state_id is linked to any State object
    if state is None:
        abort(404)

    # Check if the request body is valid JSON
    if not request.is_json:
        abort(400, description='Not a JSON')

    # Get the JSON data from the request body
    data = request.get_json()

    # Update the State object with valid key-value pairs
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    # Save the updated State object
    storage.save()

    # Return the updated State object with status code 200
    return jsonify(state.to_dict()), 200
