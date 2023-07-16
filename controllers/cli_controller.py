from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.company import Company
from models.performance import Performance
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
        ),
        User (
            username='User1',
            password=bcrypt.geneate_password_hash('user1').decode('utf-8'),
            email='user1@mail.com',
            date_created=date.today(),
            is_admin=False
        )
    ]

    db.sesion.add_all(users)

    companies = [
        Company (
            name='ADT',
            location='SA',
            artistic_director='Dan Riley'
        ),
        Company (
            name='ADC',
            location='QLD',
            artiistic_director='Amy Hollingsworth'
        )
    ]

    performances = [
        Performance (
            company_id=companies[1],
            title='Lucie in the Sky',
            date=16/07/2023,
            artform='Dance'

        )
    ]
    db.session.add_all(companies)


    db.session.commit()

    print('Tables seeded')