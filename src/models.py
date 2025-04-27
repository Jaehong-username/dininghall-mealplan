# models.py - Contains all definitions for database tables
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
import datetime
from flask import current_app, Blueprint
from flask_bcrypt import Bcrypt
import os
from datetime import datetime, timezone

# Database located in src/data/database.db

# SQLAlchemy is a python library that presents SQL tables as Python objects
# It makes things easier to use by not requiring code to have manually written SQL queries
# And is also more secure as it reduces the possibility of SQL injection attacks.
db = SQLAlchemy()
bcrypt = Bcrypt() # needed for password hashing

models_bp = Blueprint('models_bp', __name__)

# ---------- [ENTITY SETS] ----------
# User account table
class User(UserMixin, db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True) ## auto increments!
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable = False)

    # 2FA secret key for each usre
    twofa_secret = db.Column(db.String(32))

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
        
# Admin table (only one admin in system)
class Admin(db.Model):
    __tablename__ = "admin"
    admin_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.manager_id'))                 # foreign key to manager (one-to-one)

# Manager table
class Manager(db.Model):
    __tablename__ = "manager"
    manager_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)

    # relationships
    menus = db.relationship('Menu', secondary='managers_menus', back_populates='managers')  # many-to-many w/ menu
    meals = db.relationship('Meal', secondary='managers_meals', back_populates='managers')  # many-to-many w/ meals

# Student table
class Student(db.Model):
    __tablename__ = "student"
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
    balance = db.Column(db.Float, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'))                       # foreign key to admin (many-to-one)
    plan_id = db.Column(db.Integer, db.ForeignKey('meal_plan.id'))                          # vars for managing meal plan

    def __init__(self, user_id, balance):
        self.user_id = user_id
        self.balance = balance
        plan_id = 0                                                                         # initialize to 0, student can choose meal plan in manage meal plan page
    
    def get_student_by_id(uid):
        st = Student.query.filter_by(user_id = uid).first()
        
        if st is not None:
            return st
        else:
            return None

    # relationships
    user = db.relationship('User')
    meals = db.relationship('Meal', secondary='students_meals', back_populates='students')  # many-to-many w/ meals
    menus = db.relationship('Menu', secondary='students_menus', back_populates='students')  # many-to-many w/ menus

# Employee table
class Employee(db.Model):
    __tablename__ = "employee"
    employee_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))                               # foreign key to menu (many-to-one)

    # relationships
    meals = db.relationship('Meal', secondary='employees_meals', back_populates='employees') # many-to-many w/ meals

# Meal Plan table for managing a student's plan
class Meal_Plan(db.Model):
    __tablename__ = 'meal_plan'                                                             # fixing errors with naming
    id = db.Column(db.Integer, primary_key=True)                                            # simplifying primary key to id
    price = db.Column(db.Float, nullable=False)

# Menu table
class Menu(db.Model):
    __tablename__ = "menu"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String, nullable=False)

    # constructor
    def __init__(self, date, location):
        self.date = date
        self.location = location

    # relationships
    meal_categories = db.relationship('Meal_Category', secondary='menu_meal_categories', back_populates='menus')    # multi-valued attribute
    meals = db.relationship('Meal', secondary='menu_meals', back_populates='menus')                                 # multi-valued attribute
    students = db.relationship('Student', secondary='students_menus', back_populates='menus')                       # many-to-many w/ student
    managers = db.relationship('Manager', secondary='managers_menus', back_populates='menus')                       # many-to-many w/ manager

# Meal table
class Meal(db.Model):
    __tablename__ = "meal"
    id = db.Column(db.Integer, primary_key=True)
    meal_name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    number_sold = db.Column(db.Integer, nullable=False)
    
    #newly addedfor the comment :  

    # constructor
    def __init__(self, meal_name, price, number_sold):
        self.meal_name = meal_name
        self.price = price
        self.number_sold = number_sold

    # relationships
    categories = db.relationship('Meal_Category', secondary='meal_meal_categories', back_populates='meals')                    # assigining each meal to a category
    types = db.relationship('Meal_Type', secondary="meal_types", back_populates='meals')                                       # each meal can have a type
    
    menus = db.relationship('Menu', secondary='menu_meals', back_populates='meals')                                            # multi-valued attribute
    restrictions = db.relationship('Dietary_Restriction', secondary='meal_dietary_restrictions', back_populates='meals')       # multi-valued attribute
    infos = db.relationship('Nutritional_Information', secondary='meal_nutritional_informations', back_populates='meals')      # multi-valued attribute
    students = db.relationship('Student', secondary='students_meals', back_populates='meals')                                  # many-to-many w/ students
    managers = db.relationship('Manager', secondary='managers_meals', back_populates='meals')                                  # many-to-many w/ managers
    employees = db.relationship('Employee', secondary='employees_meals', back_populates='meals')                               # many-to-many w/ employees
    comments = db.relationship('Comment', back_populates='meal')

# Meal_Category (multi-valued) table for Menu
class Meal_Category(db.Model):
    __tablename__ = 'meal_category'                                                # fixing errors with naming
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String, nullable=False)

    # relationships
    menus = db.relationship('Menu', secondary='menu_meal_categories', back_populates='meal_categories')         # multi-valued attribute
    meals = db.relationship('Meal', secondary='meal_meal_categories', back_populates='categories')              # each meal can have category
    types = db.relationship('Meal_Type', secondary="meal_category_types", back_populates='categories')          # each meal can have a type

# Meal_Type (for assigning each category a type; can be multiple)
class Meal_Type(db.Model):
    __tablename__ = 'meal_type'
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String, nullable=False)

    # relationships
    categories = db.relationship('Meal_Category', secondary='meal_category_types', back_populates='types')      # each category can have a type
    meals = db.relationship('Meal', secondary="meal_types", back_populates='types')                             # each meal can have a type

# Dietary_Restrictions (multi-valued) table for Meal
class Dietary_Restriction(db.Model):
    __tablename__ = 'dietary_restriction'                                                   # fixing errors with naming
    id = db.Column(db.Integer, primary_key = True)
    restriction = db.Column(db.String, nullable=False)

    # relationships
    meals = db.relationship('Meal', secondary='meal_dietary_restrictions', back_populates='restrictions')       # multi-valued attribute               

# Nutritional_Information (multi-valued) table for Meal
class Nutritional_Information(db.Model):
    __tablename__ = 'nutritional_information'                                               # fixing errors with naming
    id = db.Column(db.Integer, primary_key = True)
    info = db.Column(db.String, nullable=False)

    # relationships
    meals = db.relationship('Meal', secondary='meal_nutritional_informations', back_populates='infos')          # multi-valued attribute


class Comment(db.Model):
    __tablename__ = 'comments'
    # Primary key for each comment
    id = db.Column(db.Integer, primary_key=True) #make it autom incremented
    content = db.Column(db.String(500), nullable=False)
    # Timestamp when the comment was created
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    
    # Foreign key to Meal model (Many-to-One relationship)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)
    # Foreign key to User model (Many-to-One relationship)
    # TODO: update user id here once finished merging with dante's code
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    
    #The backref='comments' allows you to access all comments related to a specific meal, e.g., meal.comments.
    # Relationship to the Meal model a meal can have many comments
    meal = db.relationship('Meal', back_populates='comments')

    # Relationship to the User model  a user can write many comments
    user = db.relationship('User', backref=db.backref('user_comments', lazy=True))
    
    def __repr__(self):
        return f"<Comment {self.id} by User {self.user_id} on Meal {self.meal_id} at {self.created_at}>"




class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)


# ---------- [MULTI-VALUED ATTRIBUTE TABLES] ----------
# first attribute in quotations is the title of the table columns

# Menu & Meal_Category association table
Menu_Meal_Categories = db.Table (
    'menu_meal_categories',
    db.Column('menu_id', db.ForeignKey('menu.id'), primary_key=True),
    db.Column('category', db.ForeignKey('meal_category.id'), primary_key=True)
)

# Menu & Meal association table
Menu_Meals = db.Table (
    'menu_meals',
    db.Column('menu_id', db.ForeignKey('menu.id'), primary_key=True),
    db.Column('meal_id', db.ForeignKey('meal.id'), primary_key=True)
)

# # Meal & Dietary_Restriction association table
Meal_Dietary_Restrictions = db.Table (
    'meal_dietary_restrictions',
    db.Column('meal_id', db.ForeignKey('meal.id'), primary_key=True),
    db.Column('restriction', db.ForeignKey('dietary_restriction.id'), primary_key=True)
)

# Meal & Nutritional_Information association table
Meal_Nutritional_Informations = db.Table (
    'meal_nutritional_informations',
    db.Column('meal_id', db.ForeignKey('meal.id'), primary_key=True),
    db.Column('info', db.ForeignKey('nutritional_information.id'), primary_key=True)
)

# Meal_Category & Type
Meal_Category_Types = db.Table (
    'meal_category_types',
    db.Column('category', db.ForeignKey('meal_category.id'), primary_key=True),
    db.Column('type', db.ForeignKey('meal_type.id'), primary_key=True)
)

# Meal & Type
Meal_Types = db.Table (
    'meal_types',
    db.Column('meal_id', db.ForeignKey('meal.id'), primary_key=True),
    db.Column('type', db.ForeignKey('meal_type.id'), primary_key=True)
)

Meal_Meal_Categories = db.Table (
    'meal_meal_categories',
    db.Column('meal_id', db.ForeignKey('meal.id'), primary_key=True),
    db.Column('category', db.ForeignKey('meal_category.id'), primary_key=True)
)

# ---------- [MANY-TO-MANY RELATIONSHIP TABLES] ----------
#  Student and Meal table
Students_Meals = db.Table (
    'students_meals',
    db.Column('user_id', db.ForeignKey('student.user_id'), primary_key=True),
    db.Column('meal_id', db.ForeignKey('meal.id'), primary_key=True)
)

# Student and Menu table
Students_Menus = db.Table (
    'students_menus',
    db.Column('user_id', db.ForeignKey('student.user_id'), primary_key=True),
    db.Column('meal_id', db.ForeignKey('menu.id'), primary_key=True)
)

# Manager and Menu table
Managers_Menus = db.Table (
    'managers_menus',
    db.Column('manager_id', db.ForeignKey('manager.manager_id'), primary_key=True),
    db.Column('menu_id', db.ForeignKey('menu.id'), primary_key=True)
)

# Manager and Meal table
Managers_Meals = db.Table (
    'managers_meals',
    db.Column('manager_id', db.ForeignKey('manager.manager_id'), primary_key=True),
    db.Column('meal_id', db.ForeignKey('meal.id'), primary_key=True)
)

# Employee and Meal table
Employees_Meals = db.Table (
    'employees_meals',
    db.Column('employee_id', db.ForeignKey('employee.employee_id'), primary_key=True),
    db.Column('meal_id', db.ForeignKey('meal.id'), primary_key=True)
)