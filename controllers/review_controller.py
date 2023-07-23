from flask import Blueprint, request
from init import db, bcrypt, jwt
from models.review import Review, review_schema, reviews_schema
from models.performance import Performance
from models.user import User
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta
import functools

# Create a Blueprint for reviews
review_bp = Blueprint('review', __name__, url_prefix='/reviews')

@review_bp.route('/', methods=["GET"])
def get_all_reviews():
    reviews = Review.query.all()
    return reviews_schema.dump(reviews)

@review_bp.route('/<int:id>', methods=["GET"])
def get_one_review(id):
    review = Review.query.get(id)
    if review:
        return review_schema.dump(review)
    else:
        return {'error': f'Review not found with id {id}'}

@review_bp.route('/', methods=["POST"])
@jwt_required()
def create_review():
    body_data = request.get_json()
    review = Review(
        date=body_data.get('date'),
        review=body_data.get('review'),
        rating=body_data.get('rating'),
        performance_id=body_data.get('performance_id'),
        user_id=body_data.get('user_id')
    )
    db.session.add(review)
    db.session.commit()

    return review_schema.dump(review), 201

@review_bp.route('/<int:id>', methods=["PUT"])
@jwt_required()
@auth_as_admin
def update_review(id):
    review = Review.query.get(id)
    if review:
        body_data = request.get_json()
        review.date = body_data.get('date', review.date)
        review.review = body_data.get('review', review.review)
        review.rating = body_data.get('rating', review.rating)
        review.performance_id = body_data.get('performance_id', review.performance_id)
        review.user_id = body_data.get('user_id', review.user_id)
        db.session.commit()
        return review_schema.dump(review)
    else:
        return {'error': f'Review with id {id} not found'}, 404

@review_bp.route('/<int:id>', methods=["DELETE"])
@jwt_required()
@auth_as_admin
def delete_review(id):
    review = Review.query.get(id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return {'message': f'Review with id {id} deleted successfully'}
    else:
        return {'error': f'Review with id {id} not found'}, 404