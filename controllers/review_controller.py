from flask import Blueprint, request, jsonify
from init import db, bcrypt, jwt
from models.review import Review, review_schema, reviews_schema
from models.performance import Performance
from models.user import User
from .auth_controller import auth_as_admin
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta, datetime
import functools

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
    try:
        body_data = request.get_json()
        if not body_data or 'review' not in body_data or 'rating' not in body_data or 'performance_id' not in body_data:
            return {'error': 'Missing required fields (review, rating, performance_id)'}, 400

        review_text = body_data.get('review')
        rating = body_data.get('rating')
        performance_id = body_data.get('performance_id')

        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return {'error': 'Invalid rating. Rating must be an integer between 1 and 5.'}, 400

        user_id = get_jwt_identity()
        current_date = datetime.utcnow().date()

        review = Review(
            date=current_date,
            review=review_text,
            rating=rating,
            performance_id=performance_id,
            user_id=user_id
        )
        db.session.add(review)
        db.session.commit()

        return review_schema.dump(review), 201

    except IntegrityError:
        db.session.rollback()
        return {'error': 'Database error occurred. Please try again later.'}, 500

    except Exception as e:
        return {'error': str(e)}, 500

@review_bp.route('/<int:id>', methods=["PATCH"])
@jwt_required()
def update_review(id):
    # Get the authenticated user's ID from the JWT token
    current_user_id = get_jwt_identity()

    # Get the review from the database
    review = Review.query.get(id)

    # Check if the review exists
    if not review:
        return {'error': f'Review with id {id} not found'}, 404

    # Check if the authenticated user is the owner of the review
    if review.user_id != current_user_id:
        return {'error': 'You are not authorized to update this review'}, 403

    # Update the review if the user is authorized
    body_data = request.get_json()
    review.date = body_data.get('date', review.date)
    review.review = body_data.get('review', review.review)
    review.rating = body_data.get('rating', review.rating)
    db.session.commit()

    return review_schema.dump(review)

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