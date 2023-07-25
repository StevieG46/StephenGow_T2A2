from flask import Blueprint, request
from init import db, bcrypt, jwt
from models.company import Company, company_schema, companies_schema
from models.user import User
from .auth_controller import auth_as_admin
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta
import functools

company_bp = Blueprint('companies', __name__, url_prefix='/companies')
 
@company_bp.route('/', methods=["GET"])
def get_all_companies():
    stmt = db.select(Company).order_by(Company.id)
    companies = db.session.scalars(stmt)
    return company_schema.dump(companies)

@company_bp.route('/<int:id>', methods=["GET"])
def get_one_company(id):
        stmt = db.select(Company).filter_by(id=id)
        company = db.session.scalars(stmt)
        if company:
            return company_schema.dump(company)
        else:
             return{'error': f'User not found with id {id}'}

@company_bp.route('/', methods=["POST"])
@jwt_required()
@auth_as_admin
def create_company():
    body_data = company_schema.load(request.get_json())
    company = Company(
        name=body_data.get('name'),
        location=body_data.get('location'),
        artistic_director=body_data.get('artistic_director')
    )
    db.session.add(company)
    db.session.commit()

    return company_schema.dump(company), 201

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
    
