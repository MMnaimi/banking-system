from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = "THISisfirstFLASKapp"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bs_user:asdf;lkj@localhost:5432/banking_system'
 
db = SQLAlchemy(app)
login_manager = LoginManager(app)
from app import routes