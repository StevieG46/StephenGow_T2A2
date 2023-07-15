from flask import Blueprint
from init import db, bcrypt
from models.user import User
from datetime import date

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop.all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User (
            username='Admin',
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            email='admin@admin.com',
            date_created=date.today(),
            is_admin=True 
        )
    ]

    db.sesion.add_all(users)

    db.session.commit()

    print('Tables seeded')