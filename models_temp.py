# models.py - Contains all definitions for database tables
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
import datetime
from flask import current_app, Blueprint
from flask_bcrypt import Bcrypt
import os
from datetime import datetime

# Database located in src/data/database.db

# SQLAlchemy is a python library that presents SQL tables as Python objects
# It makes things easier to use by not requiring code to have manually written SQL queries
# And is also more secure as it reduces the possibility of SQL injection attacks.
db = SQLAlchemy() #init a connection to the database
bcrypt = Bcrypt() # needed for password hashing for security

models_bp = Blueprint('models_bp', __name__)

# User account table
class User(UserMixin, db.Model): #db.Model (base class for defining models in SQLAlchemy).
    user_id = db.Column(db.Integer, primary_key=True) ## auto increments! primary_key=True argument automatically makes the column an auto-incrementing field. 
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable = False)

    # Creates new user from email, name, and (unhashed) password
    def __init__(self, email, name, password):
        # user_id automatically set to the largest value + 1
        self.email = email
        self.name = name
        # sets password to hash
        self.password = bcrypt.generate_password_hash(password) #hashes the password

        
    def get_id(self):
        return self.user_id
    
    def test_login(email_address, password):
        if User.query.filter_by(email=email_address).count() > 0:
            user = User.query.filter_by(email=email_address).first()
            if bcrypt.check_password_hash(user.password, password):
                return user
            else:
                return None
        
# ---------- [ENTITY SETS] ----------
# Admin table (only one admin in system)
class Admin(db.Model): #It has a foreign key reference to the User table (admin_id).
    admin_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.manager_id'))                 # foreign key to manager (one-to-one)

# Manager table
class Manager(db.Model):
    manager_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)

    # many-to-many relationships
    #Students_Meals table acts as the intermediary table that holds the foreign keys referencing both the Student and Meal tables.
    menus = db.relationship('Menu', secondary='Managers_Menus')   # many-to-many w/ menu
    meals = db.relationship('Meal', secondary='Managers_Meals')   # many-to-many w/ meals


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
        
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'))                       # foreign key to admin (many-to-one)

    # vars for managing meal plan
    plan_id = db.Column(db.Integer, db.ForeignKey('meal_plan.plan_id'))                      # foreign key to specific meal plan

    # relationships
    user = db.relationship('User')
    meals = db.relationship('Meal', secondary='Students_Meals')                             # many-to-many w/ meals
    menus = db.relationship('Menu', secondary='Students_Menus')                             # many-to-many w/ menus

# Employee table
class Employee(db.Model):
    employee_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
    menu_id = db.Column(db.Date, db.ForeignKey('menu.date'))                                # foreign key to menu (many-to-one)

    # relationships
    meals = db.relationship('Meal', secondary='Employees_Meals')                            # many-to-many w/ meals

# Meal Plan table for managing a student's plan
class Meal_Plan(db.Model):
    __tablename__ = 'meal_plan'                                                             # fixing errors with naming
    plan_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)


# Menu table
class Menu(db.Model):
    date = db.Column(db.Date, primary_key=True)
    location = db.Column(db.String, nullable=False)
    
    # relationships
    meal_categories = db.relationship('Meal_Category', secondary='Menu_Meal_Categories')    # multi-valued attribute
    meals = db.relationship('Meal', secondary='Menu_Meals')  #many to many relationship                              # multi-valued attribute
    students = db.relationship('Student', secondary='Students_Menus')                       # many-to-many w/ student
    managers = db.relationship('Manager', secondary='Managers_Menus')                       # many-to-many w/ manager

# Meal table
class Meal(db.Model):
    __tablename__ = 'meal'
    meal_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False) #included the name of the food
    price = db.Column(db.Float, nullable=False)
    number_sold = db.Column(db.Integer, nullable=False)
    
    # relationships
    menus = db.relationship('Menu', secondary='Menu_Meals')                                         # multi-valued attribute
    restrictions = db.relationship('Dietary_Restriction', secondary='Meal_Dietary_Restrictions')    # multi-valued attribute
    infos = db.relationship('Nutritional_Information', secondary='Meal_Nutritional_Informations')   # multi-valued attribute
    students = db.relationship('Student', secondary='Students_Meals')                               # many-to-many w/ students
    managers = db.relationship('Manager', secondary='Managers_Meals')                               # many-to-many w/ managers
    employees = db.relationship('Employee', secondary='Employees_Meals')                   # many-to-many w/ employees
    
    
    # One-to-many relationship with Comment
    comments = db.relationship('Comment', backref='meal', lazy=True)


# Meal_Category (multi-valued) table for Menu
class Meal_Category(db.Model):
    __tablename__ = 'meal_category'                                                         # fixing errors with naming
    category = db.Column(db.String, primary_key = True)
    
    # relationships
    menus = db.relationship('Menu', secondary='Menu_Meal_Categories')                       # multi-valued attribute

# Dietary_Restrictions (multi-valued) table for Meal
class Dietary_Restriction(db.Model):
    __tablename__ = 'dietary_restriction'                                                   # fixing errors with naming
    restriction = db.Column(db.String, primary_key=True)

    # relationships
    meals = db.relationship('Meal', secondary='Meal_Dietary_Restrictions')                  # multi-valued attribute               

# Nutritional_Information (multi-valued) table for Meal
class Nutritional_Information(db.Model):
    __tablename__ = 'nutritional_information'                                               # fixing errors with naming
    info = db.Column(db.String, primary_key=True)

    # relationships
    meals = db.relationship('Meal', secondary='Meal_Nutritional_Informations')              # multi-valued attribute




class Comment(db.Model):
    __tablename__ = 'comments'
    # Primary key for each comment
    comment_id = db.Column(db.Integer, primary_key=True) #make it autom incremented
    content = db.Column(db.String(500), nullable=False)
    # Timestamp when the comment was created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    # Foreign key to Meal model (Many-to-One relationship)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.meal_id'), nullable=False)
    # Foreign key to User model (Many-to-One relationship)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    
    #The backref='comments' allows you to access all comments related to a specific meal, e.g., meal.comments.
    # Relationship to the Meal model a meal can have many comments
    meal = db.relationship('Meal', backref=db.backref('meal_comments', lazy=True))
    # Relationship to the User model  a user can write many comments
    user = db.relationship('User', backref=db.backref('user_comments', lazy=True))
    
    
    
    def __repr__(self):
        return f"<Comment {self.comment_id} by User {self.user_id} on Meal {self.meal_id} at {self.created_at}>"


# ---------- [MULTI-VALUED ATTRIBUTE TABLES] ----------


# Menu & Meal_Category association table
Menu_Meal_Categories = db.Table (
    'Menu_Meal_Categories',
    db.Column('date', db.ForeignKey('menu.date'), primary_key=True),
    db.Column('category', db.ForeignKey('meal_category.category'), primary_key=True)
)

# Menu & Meal association table
Menu_Meals = db.Table (
    'Menu_Meals',
    db.Column('date', db.ForeignKey('menu.date'), primary_key=True),
    db.Column('meal_id', db.ForeignKey('meal.meal_id'), primary_key=True)
)

# # Meal & Dietary_Restriction association table
Meal_Dietary_Restrictions = db.Table (
    'Meal_Dietary_Restrictions',
    db.Column('meal_id', db.ForeignKey('meal.meal_id'), primary_key=True),
    db.Column('restriction', db.ForeignKey('dietary_restriction.restriction'), primary_key=True)
)

# Meal & Nutritional_Information association table
Meal_Nutritional_Informations = db.Table (
    'Meal_Nutritional_Informations',
    db.Column('meal_id', db.ForeignKey('meal.meal_id'), primary_key=True),
    db.Column('info', db.ForeignKey('nutritional_information.info'), primary_key=True)
)



# ---------- [MANY-TO-MANY RELATIONSHIP TABLES] ----------
#  Student and Meal table
Students_Meals = db.Table (
    'Students_Meals',
    db.Column('user_id', db.ForeignKey('student.user_id'), primary_key=True),
    db.Column('meal_id', db.ForeignKey('meal.meal_id'), primary_key=True)
)

# Student and Menu table
Students_Menus = db.Table (
    'Students_Menus',
    db.Column('user_id', db.ForeignKey('student.user_id'), primary_key=True),
    db.Column('date', db.ForeignKey('menu.date'), primary_key=True)
)

# Manager and Menu table
Managers_Menus = db.Table (
    'Managers_Menus',
    db.Column('manager_id', db.ForeignKey('manager.manager_id'), primary_key=True),
    db.Column('date', db.ForeignKey('menu.date'), primary_key=True)
)

# Manager and Meal table
Managers_Meals = db.Table (
    'Managers_Meals',
    db.Column('manager_id', db.ForeignKey('manager.manager_id'), primary_key=True),
    db.Column('meal_id', db.ForeignKey('meal.meal_id'), primary_key=True)
)

# Employee and Meal table
Employees_Meals = db.Table (
    'Employees_Meals',
    db.Column('employee_id', db.ForeignKey('employee.employee_id'), primary_key=True),
    db.Column('meal_id', db.ForeignKey('meal.meal_id'), primary_key=True)
)






