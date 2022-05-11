from app.models import User
from flask_seeder import Seeder, Faker

class MakeAdmin(Seeder):
    def run(self):
        faker = Faker(
        cls=User, init={
            'id': 1,
            'fullname': 'admin',
            'username': 'admin',
            'email' : 'admin@gmail.com',
            'state' : 'active',
            'password': '12345678',
            'role' : 'admin',
            'gender' : 'male',
            'phone' : '0777777777',
            'birth_date': '1982-01-01'
        }
    )
    admin = User.query.filter_by(role='admin').first()
   
