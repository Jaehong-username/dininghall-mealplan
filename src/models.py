# models.py - Contains all definitions for database tables
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
import datetime
from flask import current_app, Blueprint
from flask_bcrypt import Bcrypt
import os

# Database located in src/data/database.db

# SQLAlchemy is a python library that presents SQL tables as Python objects
# It makes things easier to use by not requiring code to have manually written SQL queries
# And is also more secure as it reduces the possibility of SQL injection attacks.
db = SQLAlchemy()
bcrypt = Bcrypt() # needed for password hashing

models_bp = Blueprint('models_bp', __name__)

# User account table
class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True) ## auto increments!
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable = False)

    # Creates new user from email, name, and (unhashed) password
    def __init__(self, email, name, password):
        # user_id automatically set to the largest value + 1
        self.email = email
        self.name = name
        # sets password to hash
        self.password = bcrypt.generate_password_hash(password)

        
    def get_id(self):
        return self.user_id
    
    def test_login(email_address, password):
        if User.query.filter_by(email=email_address).count() > 0:
            user = User.query.filter_by(email=email_address).first()
            if bcrypt.check_password_hash(user.password, password):
                return user
            else:
                return None
            
# Student table
class Student(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
    balance = db.Column(db.Float, nullable=False)
    
    def __init__(self, user_id, balance):
        self.user_id = user_id
        self.balance = balance
    
    def get_student_by_id(uid):
        st = Student.query.filter_by(user_id = uid).first()
        
        if st is not None:
            return st
        else:
            return None