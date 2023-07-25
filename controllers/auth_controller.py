from flask import Blueprint, request
from init import db, bcrypt, jwt
from models.user import User, user_schema, users_schema
from flask_jwt_extended import create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta
import functools

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

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

@auth_bp.route('/register', methods=["POST"])
def auth_register():
    try:
        body_data = request.get_json()

        user = User()
        user.username = body_data.get('username')
        if body_data.get('password'):
            user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        user.email = body_data.get('email')

        db.session.add(user)
        db.session.commit()

        return user_schema.dump(user), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error': 'Email address already in use'}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The{err.orig.diag.column_name} is required'},409

@auth_bp.route('/login', methods=["POST"])
def auth_login():
    body_data = request.get_json()

    stmt = db.select(User).filter_by(email=body_data.get('email'))
    user = db.session.scalar(stmt)

    if user and bcrypt.check_password_hash(user.password, body_data.get('password')):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=7))
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}
    else:
        return {'error': 'Invalid email or password'}, 401
    
