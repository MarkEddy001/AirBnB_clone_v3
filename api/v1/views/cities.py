#!/usr/bin/python3
"""Modules for city-related endpoints"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from datetime import datetime
import uuid


@app_views.route('/states/<state_id>/cities', methods=['GET'])
@app_views.route('/states/<state_id>/cities/', methods=['GET'])
def list_cities_of_state(state_id):
    """Fetches a list of all City objects"""
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    list_cities = [obj.to_dict() for obj in storage.all("City").values()
                   if state_id == obj.state_id]
    return jsonify(list_cities)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_city(state_id):
    """Creates a City and associates"""
    # Check if state_id is linked to any State object
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    # Check if the request body is valid JSON
    if not request.is_json:
        abort(400, description='Not a JSON')

    # Get the JSON data from the request body
    data = request.get_json()

    # Check if the dictionary contains the key 'name'
    if 'name' not in data:
        abort(400, description='Missing name')

    # Create a new City linked to the State
    new_city = City(**data)
    new_city.state_id = state.id
    storage.new(new_city)
    storage.save()

    # Return the new City with status code 201
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieves a City object"""
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if city_obj == []:
        abort(404)
    return jsonify(city_obj[0])


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object"""
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if city_obj == []:
        abort(404)
    city_obj.remove(city_obj[0])
    for obj in all_cities:
        if obj.id == city_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'])
def updates_city(city_id):
    """Updates a specific City object"""
    city = storage.get(City, city_id)

    # Check if city_id is linked to any City object
    if city is None:
        abort(404)

    # Check if the request body is valid JSON
    if not request.is_json:
        abort(400, description='Not a JSON')

    # Get the JSON data from the request body
    data = request.get_json()

    # Update the City object with valid key-value pairs
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    # Save the updated City object
    storage.save()

    # Return the updated City object with status code 200
    return jsonify(city.to_dict()), 200
