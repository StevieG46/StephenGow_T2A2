from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.company import Company
from models.performance import Performance
from models.review import Review
from datetime import date

db_commands = Blueprint('db', __name__)

# T0 create tables. use - flask db create
# To seed tables. use - flask db seed
# To drop tables. use - flask db drop

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
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
            password=bcrypt.generate_password_hash('user1').decode('utf-8'),
            email='user1@mail.com',
            date_created=date.today(),
            is_admin=False
        )
    ]

    db.session.add_all(users)

    companies = [
        Company (
            name='ADT',
            location='SA',
            artistic_director='Dan Riley'
        ),
        Company (
            name='ADC',
            location='QLD',
            artistic_director='Amy Hollingsworth'
        )
    ]
    db.session.add_all(companies)
    
    db.session.commit()

    performances = [
        Performance (
            company_id=(companies[1].id),
            title='Lucie in the Sky',
            date=date(2023, 7, 16),
            artform='Dance'
        )
    ]
    db.session.add_all(performances)
    db.session.commit()

    reviews = [
        Review (
            date=date.today(),
            review='A great performance with integrated used of drones and dancers',
            rating=4,
            performance_id=(performances[0].id),
            user_id=(users[1].id)
        )

    ]
    db.session.add_all(reviews)

    db.session.commit()

    print('Tables seeded')