from flask import Blueprint, request
from init import db, bcrypt, jwt, ma
from models.company import Company, company_schema, companies_schema
from models.user import User
from .auth_controller import auth_as_admin
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from psycopg2 import errorcodes
from datetime import timedelta
import functools

company_bp = Blueprint('companies', __name__, url_prefix='/companies')
 
#  Gets all companies, access open to all.
@company_bp.route('/', methods=["GET"])
def get_all_companies():
    stmt = db.select(Company).order_by(Company.id)
    companies = db.session.scalars(stmt)
    return company_schema.dump(companies)

#  Gets single company by id, access open to all.
@company_bp.route('/<int:id>', methods=["GET"])
def get_one_company(id):
        stmt = db.select(Company).filter_by(id=id)
        company = db.session.scalars(stmt)
        if company:
            return company_schema.dump(company)
        else:
             return{'error': f'User not found with id {id}'}

# Creates new company, Admin Token required. 
# Fields required, name, location & artistic_director.
@company_bp.route('/', methods=["POST"])
@jwt_required()
@auth_as_admin
def create_company():
    try:
        body_data = request.get_json()

        errors = company_schema.validate(body_data)
        if 'name' not in body_data:
            errors['name'] = ['Name is required.']

        if errors:
            return {'errors': errors}, 400

        company = Company(
            name=body_data['name'],
            location=body_data.get('location'),
            artistic_director=body_data.get('artistic_director')
        )
        db.session.add(company)
        db.session.commit()

        return company_schema.dump(company), 201

    except IntegrityError:
        db.session.rollback()
        return {'error': 'Database error occurred. Please try again later.'}, 500

    except ValidationError as e:
        return {'error': e.messages}, 400

    except Exception as e:
        return {'error': str(e)}, 500

# Edits company by id, Admin Token required. 
# Fields required, one or more, name, location & artistic_director.
@company_bp.route('/<int:id>', methods=["PATCH"])
@jwt_required()
@auth_as_admin
def update_company(id):
    try:
        company = Company.query.get(id)

        if not company:
            return {'error': f'Company not found with id {id}'}, 404

        body_data = request.get_json()

        if 'location' in body_data:
            company.location = body_data['location']

        if 'artistic_director' in body_data:
            company.artistic_director = body_data['artistic_director']

        db.session.commit()

        return company_schema.dump(company), 200

    except IntegrityError:
        db.session.rollback()
        return {'error': 'Database error occurred. Please try again later.'}, 500

    except Exception as e:
        return {'error': str(e)}, 500

# Deletes Company by id, Admin Token required. 
# Fields required, name, location & artistic_director.
@company_bp.route('/<int:id>', methods=["DELETE"])
@jwt_required()
@auth_as_admin
def delete_company(id):
    stmt = db.select(Company).filter_by(id=id)
    company = db.session.scalar(stmt)
    if company:
        db.session.delete(company)
        db.session.commit()
        return{'message': f'Company {company.name} deleted successfully'}
    else:
        return{'error': f'Company with id {id} not found'}, 404