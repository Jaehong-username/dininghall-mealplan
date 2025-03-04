# models.py - Contains all definitions for database tables
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
from flask import current_app
from flask_bcrypt import Bcrypt
import os

# SQLite Viewer on the vscode extension marketplace is a useful free tool to preview db files
# Database located in src/data/database.db

# SQLAlchemy is a python library that presents SQL tables as Python objects
# It makes things easier to use by not requiring code to have manually written SQL queries
# And is also more secure as it reduces the possibility of SQL injection attacks.
db = SQLAlchemy()
bcrypt = Bcrypt() # needed for password hashing

### --- Initialize databases --- ###
# Tables are created dynamically at first run w/ SQLAlchemy.
# Don't commit database file to git!

# User account table
class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True) ## auto increments!
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable = False)

    def __init__(self, email, name, password):
        # user_id automatically set to the largest value + 1
        self.email = email
        self.name = name
        self.password = bcrypt.generate_password_hash(password)
    
# Student table
class Student(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
    balance = db.Column(db.Float, nullable=False)