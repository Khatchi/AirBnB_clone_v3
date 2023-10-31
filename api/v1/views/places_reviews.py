#!/usr/bin/python3
"""Implement API endpoints for Review objects"""
from flask import abort, make_response, request
from api.v1.views import app_views
import json
from models.user import User
from models.place import Place
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_reviews(place_id=None, review_id=None):
    """Retrieves the list of all Review objects of a Place,
    or a specific Review by ID.
    """
    if review_id:
        review = storage.get(Review, review_id)
        if not review:
            abort(404)
        res_obj = review.to_dict()
    else:
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        reviews_list = []
        for review in place.reviews:
            reviews_list.append(review.to_dict())
        res_obj = reviews_list

    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object by ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    res_obj = {}
    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Creates a new Review object in a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    new_review = Review(**data)
    new_review.place_id = place.id
    new_review.save()
    res_obj = new_review.to_dict()
    response = make_response(json.dumps(res_obj), 201)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates a Review object by ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    # Update the Review object with the new data
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    review.save()

    res_obj = review.to_dict()
    response = make_response(json.dumps(res_obj), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
