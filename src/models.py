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
    __tablename__ = 'user'
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

    def to_dict(self):
        # Return table data in a json-ifiable format
        # Exclamations are used to put primary keys at the front of the list, since JSON sorts keys alphabetically.
        # They shouldn't be used for other parameters and should be trimmed in frontend code if necessary.
        return {
            '!id': self.user_id,
            'email': self.email,
            'name': self.name,
            'password': str(self.password)
        }
        
    def get_id(self):
        return self.user_id
    
    def test_login(email_address, password):
        if User.query.filter_by(email=email_address).count() > 0:
            user = User.query.filter_by(email=email_address).first()
            if bcrypt.check_password_hash(user.password, password):
                return user
            else:
                return None
            
    def is_admin(self):
        if(Admin.get_admin_by_id(self.user_id) is not None):
            return True
        else:
            return False

# ---------- [ENTITY SETS] ----------
# Admin table (only one admin in system)
class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.manager_id'))        
    
    def to_dict(self):
        # Return table data in a json-ifiable format
        return {
            "!admin_id": self.admin_id,
            "manager_id": self.manager_id
        }
    
    def get_admin_by_id(uid):
        ad = Admin.query.filter_by(admin_id = uid).first()
        
        if ad is not None:
            return ad
        else:
            return None

# Manager table
class Manager(db.Model):
    __tablename__ = 'manager'
    manager_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)

    def to_dict(self):
        # Return table data in a json-ifiable format
        return {
            "manager_id": self.manager_id
        }

    # relationships
    menus = db.relationship('Menu', secondary='Managers_Menus')                             # many-to-many w/ menu
    meals = db.relationship('Meal', secondary='Managers_Meals')                             # many-to-many w/ meals

# Student table
class Student(db.Model):
    __tablename__ = 'student'
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
    balance = db.Column(db.Float, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'))  # foreign key to admin (many-to-one)
    # vars for managing meal plan
    plan_id = db.Column(db.Integer, db.ForeignKey('meal_plan.plan_id')) # foreign key to specific meal plan

    def to_dict(self):
        # Return table data in a json-ifiable format
        return {
            "!user_id": self.user_id,
            "balance": self.balance,
            "admin_id": self.admin_id,
            "plan_id": self.plan_id
        }

    # relationships
    user = db.relationship('User')
    meals = db.relationship('Meal', secondary='Students_Meals') # many-to-many w/ meals
    menus = db.relationship('Menu', secondary='Students_Menus') # many-to-many w/ menus
    
    
    def get_student_by_id(uid):
        st = Student.query.filter_by(user_id = uid).first()
        
        if st is not None:
            return st
        else:
            return None

# Employee table
class Employee(db.Model):
    __tablename__ = 'employee'
    employee_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
    menu_id = db.Column(db.Date, db.ForeignKey('menu.date'))                                # foreign key to menu (many-to-one)

    def to_dict(self):
        # Return table data in a json-ifiable format
        return {
            "!employee_id": self.employee_id,
            "menu_id": self.menu_id
        }

    # relationships
    meals = db.relationship('Meal', secondary='Employees_Meals')                            # many-to-many w/ meals

# Meal Plan table for managing a student's plan
class Meal_Plan(db.Model):
    __tablename__ = 'meal_plan'                                                             # fixing errors with naming
    plan_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        # Return table data in a json-ifiable format
        return {
            "!plan_id": self.plan_id,
            "price": self.price
        }

    

# Menu table
class Menu(db.Model):
    __tablename__ = 'menu'
    date = db.Column(db.Date, primary_key=True)
    location = db.Column(db.String, nullable=False)
    
    # relationships
    meal_categories = db.relationship('Meal_Category', secondary='Menu_Meal_Categories')    # multi-valued attribute
    meals = db.relationship('Meal', secondary='Menu_Meals')                                 # multi-valued attribute
    students = db.relationship('Student', secondary='Students_Menus')                       # many-to-many w/ student
    managers = db.relationship('Manager', secondary='Managers_Menus')       # many-to-many w/ manager
    
    def to_dict(self):
        # Return table data in a json-ifiable format
        return {
            "date": self.date,
            "location": self.location
        }

# Meal table
class Meal(db.Model):
    __tablename__ = 'meal'
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
    
    def to_dict(self):
        # Return table data in a json-ifiable format
        return {
            "!meal_id": self.meal_id,
            "price": self.price,
            "number_sold": self.number_sold
        }

# Meal_Category (multi-valued) table for Menu
class Meal_Category(db.Model):
    __tablename__ = 'meal_category'                                                         # fixing errors with naming
    category = db.Column(db.String, primary_key = True)
    
    # relationships
    menus = db.relationship('Menu', secondary='Menu_Meal_Categories')                       # multi-valued attribute
    def to_dict(self):
        # Return table data in a json-ifiable format
        return {
            "category": self.category
        }

# Dietary_Restrictions (multi-valued) table for Meal
class Dietary_Restriction(db.Model):
    __tablename__ = 'dietary_restriction'                                                   # fixing errors with naming
    restriction = db.Column(db.String, primary_key=True)

    # relationships
    meals = db.relationship('Meal', secondary='Meal_Dietary_Restrictions')                  # multi-valued attribute               
    def to_dict(self):
        # Return table data in a json-ifiable format
        return {
            "restriction": self.restriction
        }

# Nutritional_Information (multi-valued) table for Meal
class Nutritional_Information(db.Model):
    __tablename__ = 'nutritional_information'                                               # fixing errors with naming
    info = db.Column(db.String, primary_key=True)

    # relationships
    meals = db.relationship('Meal', secondary='Meal_Nutritional_Informations')              # multi-valued attribute
    def to_dict(self):
        # Return table data in a json-ifiable format
        return {
            "info": self.info
        }

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