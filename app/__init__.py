from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder


app = Flask(__name__)
app.config['SECRET_KEY'] = "THISisfirstFLASKapp"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bs_user:asdf;lkj@localhost:5432/banking_system'
 
db = SQLAlchemy(app)
migrate = Migrate(app, db)
seeder = FlaskSeeder(app, db)

login_manager = LoginManager(app)
from app import users
from app import system_user