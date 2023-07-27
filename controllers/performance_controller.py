from flask import Blueprint, request, jsonify
from init import db, bcrypt, jwt
from models.performance import Performance, performance_schema, performances_schema
from models.company import Company
from models.review import reviews_schema
from models.user import User
from .auth_controller import auth_as_admin
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from psycopg2 import errorcodes
from datetime import timedelta
import functools

performance_bp = Blueprint('performances', __name__, url_prefix='/performances')

# Gets all performances, access open to all.
@performance_bp.route('/', methods=["GET"])
def get_all_performances():
    performances = Performance.query.all()
    return performances_schema.dump(performances)

# Gets single performance by id, access open to all.
@performance_bp.route('/<int:id>', methods=["GET"])
def get_one_performance(id):
    performance = Performance.query.get(id)
    if performance:
        performance_data = performance_schema.dump(performance)
        reviews_data = [{'id': review.id, 'review': review.review} for review in performance.reviews]
        performance_data['reviews'] = reviews_data
        return jsonify(performance_data)
    else:
        return {'error': f'Performance not found with id {id}'}

# Creates performance - Admin token required.
# Fields required, company_id, title, date, artform.
@performance_bp.route('/', methods=["POST"])
@jwt_required()
@auth_as_admin
def create_performance():
    try:
        body_data = request.get_json()

        errors = performance_schema.validate(body_data)
        
        if 'company_id' not in body_data:
            errors['company_id'] = ['Company ID is required.']
        if 'title' not in body_data:
            errors['title'] = ['Title is required.']
        if errors:
            return {'errors': errors}, 400

        company_id = body_data['company_id']

        if not db.session.query(Company.id).filter_by(id=company_id).scalar():
            return {'error': f'Company with ID {company_id} does not exist.'}, 404

        performance = Performance(
            company_id=company_id,
            title=body_data['title'],
            date=body_data.get('date'),
            artform=body_data.get('artform')
        )
        db.session.add(performance)
        db.session.commit()

        return performance_schema.dump(performance), 201

    except IntegrityError:
        db.session.rollback()
        return {'error': 'Database error occurred. Please try again later.'}, 500

    except ValidationError as e:
        return {'error': e.messages}, 400

    except SQLAlchemyError:
        db.session.rollback()
        return {'error': 'Database error occurred. Please try again later.'}, 500

    except Exception as e:
        return {'error': str(e)}, 500
    
# Edits single performance, admin token required.
# Fields required, one or more,  company_id, title, date, artform.
@performance_bp.route('/<int:id>', methods=["PATCH"])
@jwt_required()
@auth_as_admin
def update_performance(id):
    try:
        performance = Performance.query.get(id)

        if not performance:
            return {'error': f'Performance not found with id {id}'}, 404

        body_data = request.get_json()

        company_id = body_data['company_id']

        if not db.session.query(Company.id).filter_by(id=company_id).scalar():
            return {'error': f'Company with ID {company_id} does not exist.'}, 404

        performance.company_id = company_id
        performance.title = body_data['title']
        performance.date = body_data.get('date', performance.date)
        performance.artform = body_data.get('artform', performance.artform)

        db.session.commit()

        return performance_schema.dump(performance), 200

    except IntegrityError:
        db.session.rollback()
        return {'error': 'Database error occurred. Please try again later.'}, 500
    except ValidationError as e:
        return {'error': e.messages}, 400
    except SQLAlchemyError:
        db.session.rollback()
        return {'error': 'Database error occurred. Please try again later.'}, 500
    except Exception as e:
        return {'error': str(e)}, 500


# Deletes performance by id, admin token required.
@performance_bp.route('/<int:id>', methods=["DELETE"])
@jwt_required()
@auth_as_admin
def delete_performance(id):
    performance = Performance.query.get(id)
    if performance:
        db.session.delete(performance)
        db.session.commit()
        return {'message': f'Performance {performance.title} deleted successfully'}
    else:
        return {'error': f'Performance with id {id} not found'}, 404