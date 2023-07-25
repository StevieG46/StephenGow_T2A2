from flask import Blueprint, request
from init import db, bcrypt, jwt
from models.user import User, user_schema, users_schema
from .auth_controller import auth_as_admin
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta
import functools

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/', methods=["GET"])
def get_all_users():
    stmt = db.select(User).order_by(User.id)
    users = db.session.scalars(stmt)
    return user_schema.dump(users)

@user_bp.route('/<int:id>', methods=["GET"])
def get_one_user(id):
        stmt = db.select(User).filter_by(id=id)
        user = db.session.scalars(stmt)
        if user:
            return user_schema.dump(user)
        else:
             return{'error': f'User not found with id {id}'}

@user_bp.route('/<int:id>', methods=["DELETE"])
@jwt_required()
@auth_as_admin
def delete_user(id):
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return{'message': f'User {user.username} deleted succesfully'}
    else:
        return{'error': f'User with id {id} not found'}, 404