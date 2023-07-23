from flask import Blueprint, request
from init import db, bcrypt, jwt
from models.performance import Performance, performance_schema, performances_schema
from models.user import User
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta
import functools

performance_bp = Blueprint('performances', __name__, url_prefix='/performances')

def auth_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user.is_admin:
            return fn(*args, **kwargs)
        else:
            return {'error': 'Not authorised to peform this delete'}, 403
    return wrapper

@performance_bp.route('/', methods=["GET"])
def get_all_performances():
    performances = Performance.query.all()
    return performances_schema.dump(performances)

@performance_bp.route('/<int:id>', methods=["GET"])
def get_one_performance(id):
    performance = Performance.query.get(id)
    if performance:
        return performance_schema.dump(performance)
    else:
        return {'error': f'Performance not found with id {id}'}

@performance_bp.route('/', methods=["POST"])
@jwt_required()
@auth_as_admin
def create_performance():
    body_data = performance_schema.load(request.get_json())
    performance = Performance(
        company_id=body_data.get('company_id'),
        title=body_data.get('title'),
        date=body_data.get('date'),
        artform=body_data.get('artform')
    )
    db.session.add(performance)
    db.session.commit()

    return performance_schema.dump(performance), 201

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