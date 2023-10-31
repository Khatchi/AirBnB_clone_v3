from flask import abort, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
import json
from flask_cors import CORS

CORS(app_views, resources={r"/api/v1/places_amenities/*": {"origins": "0.0.0.0"}})

@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects linked to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities_list = []
    if storage.get_type() == "db":
        amenities_list = [amenity.to_dict() for amenity in place.amenities]
    elif storage.get_type() == "file":
        for amenity_id in place.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenities_list.append(amenity.to_dict())
    return make_response(json.dumps(amenities_list), 200)

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Deletes an Amenity object linked to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity not in place.amenities and amenity_id not in place.amenity_ids:
        abort(404)
    if storage.get_type() == "db":
        place.amenities.remove(amenity)
    elif storage.get_type() == "file":
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return make_response(json.dumps({}), 200)

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_place_amenity(place_id, amenity_id):
    """Links an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity in place.amenities or amenity_id in place.amenity_ids:
        if storage.get_type() == "db":
            return make_response(json.dumps(amenity.to_dict()), 200)
        elif storage.get_type() == "file":
            return make_response(json.dumps(amenity.to_dict()), 200)
    if storage.get_type() == "db":
        place.amenities.append(amenity)
    elif storage.get_type() == "file":
        place.amenity_ids.append(amenity_id)
    storage.save()
    return make_response(json.dumps(amenity.to_dict()), 201)
