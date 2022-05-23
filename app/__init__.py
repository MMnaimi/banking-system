from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = "THISisfirstFLASKapp"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bs_user:asdf;lkj@localhost:5432/banking_system'
 
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Mail configuration
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'a9c581f2f8e0ad'
app.config['MAIL_PASSWORD'] = '2c364752d8abd8'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

login_manager = LoginManager(app)
from app import users
from app import system_user

