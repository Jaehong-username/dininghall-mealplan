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

# ---------- [ENTITY SETS] ----------
# Admin table (only one admin in system)
class Admin(db.Model):
    admin_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.manager_id'))                 # foreign key to manager (one-to-one)

# Manager table
class Manager(db.Model):
    manager_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)

    # relationships
    menus = db.relationship('Menu', secondary='Managers_Menus')                             # many-to-many w/ menu
    meals = db.relationship('Meal', secondary='Managers_Meals')                             # many-to-many w/ meals

# Student table
class Student(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
    balance = db.Column(db.Float, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'))                       # foreign key to admin (many-to-one)

    # vars for managing meal plan
    plan_id = db.Column(db.Integer, db.ForeignKey('mealplan.plan_id'))                      # foreign key to specific meal plan

    # relationships
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
    plan_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)

# Menu table
class Menu(db.Model):
    date = db.Column(db.Date, primary_key=True)
    location = db.Column(db.String, nullable=False)
    
    # relationships
    meal_categories = db.relationship('Meal_Category', secondary='Menu_Meal_Categories')    # multi-valued attribute
    meals = db.relationship('Meal', secondary='Menu_Meals')                                 # multi-valued attribute
    students = db.relationship('Student', secondary='Students_Menus')                       # many-to-many w/ student
    managers = db.relationship('Manager', secondary='Managers_Menus')                       # many-to-many w/ manager

# Meal table
class Meal(db.Model):
    meal_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    number_sold = db.Column(db.Integer, nullable=False)

    # relationships
    menus = db.relationship('Menu', secondary='Menu_Meals')                                         # multi-valued attribute
    restrictions = db.relationship('Dietary_Restriction', secondary='Meal_Dietary_Restrictions')    # multi-valued attribute
    infos = db.relationship('Nutritional_Information', secondary='Meal_Nutritional_Informations')   # multi-valued attribute
    students = db.relationship('Student', secondary='Students_Meals')                               # many-to-many w/ students
    managers = db.relationship('Manager', secondary='Managers_Meals')                               # many-to-many w/ managers
    employees = db.relationship('Employee', secondary='Employees_Meals')                            # many-to-many w/ employees

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