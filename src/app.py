#flask library packages
from flask import Flask, render_template, url_for, redirect, flash, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask_login import UserMixin,LoginManager, login_user, logout_user, current_user, login_required
# Flask forms extension packages
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, InputRequired, ValidationError
from flask_bcrypt import Bcrypt
import secrets
from models import *
from form_classes import *
from views import *
from api import *
from datetime import date

#import related to uploading images
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "data/database.db")
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/14253/Desktop/dininghall-mealplan-1/data/database.db'
bcrypt = Bcrypt(app)

# image upload setup
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')


# Create secret key
secret = secrets.token_urlsafe(16)
app.config['SECRET_KEY'] = secret
csrf = CSRFProtect(app)

app.register_blueprint(views)
app.register_blueprint(models_bp)
app.register_blueprint(api_bp)

# Create all databases if they don't exist
db.init_app(app)

# Enable foreign key constraints for SQLite every query connection.
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# sample data for database
def create_db():
    with app.app_context():
        db.drop_all()  # This will drop all tables from the database
        db.create_all()

        with db.session.no_autoflush:
            # TEMP STUDENT FOR TESTING PURPOSES (since no info in database yet)
            # to clean out (ONLY DO WITH NON-IMPORTANT DB): rm database.db & rerun code after commenting code out
            # TEMP STUDENT FOR TESTING PURPOSES (since no info in database yet)
            existing_user = User.query.filter_by(user_id=1).first()
            if existing_user:
                print("Temp user exists")
            else:
                temp_user = User(
                    name="test",
                    email="test@email.com",
                    password="test"
                )
                
                admin_user = User(
                    name="admin",
                    email="admin@email.com",
                    password="admin"
                )

                employee_user = User(
                    name="employee",
                    email="employee@email.com",
                    password="employee"
                )

                manager_user = User(
                    name="manager",
                    email="manager@email.com",
                    password="manager"
                )

                db.session.add(temp_user)
                db.session.add(admin_user)
                db.session.add(employee_user)
                db.session.add(manager_user)
                db.session.commit()

                temp_admin = Admin(
                    admin_id=admin_user.user_id
                )

                temp_employee = Employee(
                    employee_id=employee_user.user_id
                )

                temp_manager = Manager(
                    manager_id=manager_user.user_id
                )

                db.session.add(temp_admin)
                db.session.add(temp_employee)
                db.session.add(temp_manager)
                db.session.commit()
            
                temp_student = Student(
                    user_id=temp_user.user_id,
                    balance=1000.00,
                    admin_id=temp_admin.admin_id,
                    plan_id=None
                )
            
                db.session.add(temp_student)
                db.session.commit()

            # BASE TYPES FOR TESTING
            base_types = ["Breakfast", "Lunch", "Brunch", "Dinner"]
            for type in base_types:
                existing_type = Meal_Type.query.filter_by(type=type).first()
                if not existing_type:
                    new_type = Meal_Type(type=type)
                    db.session.add(new_type)
                
            db.session.commit()

            # BASE CATEGORIES FOR TESTING
            # TODO: add location-exclusive category checks?  
            # TODO: check if category contains no meals before printing?
            base_categories = {
                "Bakery": ["Breakfast", "Brunch", "Lunch", "Dinner"],
                "Build-a-Breakfast Sandwich": ["Breakfast", "Brunch"],
                "Chef's Creation": ["Breakfast", "Brunch", "Lunch", "Dinner"],
                "Hot Cereal": ["Breakfast", "Brunch"],
                "Big Cat Grille": ["Brunch", "Lunch", "Dinner"],
                # "Build-a-Sandwich": ["Lunch", "Dinner"],
                # "Grapevine": ["Lunch", "Dinner"],
                # "Hot Spot": ["Lunch", "Dinner"],
                "Deli": ["Brunch", "Lunch", "Dinner"],
                # "Grill": ["Lunch", "Dinner"],
                "Natural": ["Brunch", "Lunch", "Dinner"],
                # "On Fire": ["Lunch", "Dinner"],
                # "Salad Bar Fruits": ["Lunch", "Dinner"],
                "Presto Pizza": ["Brunch", "Lunch", "Dinner"],
                "Salads": ["Brunch", "Lunch", "Dinner"],
                "Soups": ["Lunch", "Dinner"],
                # "Stonewall Pasta": ["Lunch", "Dinner"],
                # "Stonewall Pizza": ["Lunch", "Dinner"]
            }

            # adding categories to meal_category
            for category, types in base_categories.items():

                # adding categories
                existing_category = Meal_Category.query.filter_by(category=category).first()
                if not existing_category:
                    new_category = Meal_Category(category=category)
                    db.session.add(new_category)
                    existing_category = new_category

                # adding relationships with type
                for type in types:
                    existing_type = Meal_Type.query.filter_by(type=type).first()
                    if existing_type:
                        if existing_type not in existing_category.types:
                            existing_category.types.append(existing_type)

            db.session.commit()

            # MEAL ATTRIBUTES FOR TESTING PURPOSES
            base_nutritional = ["Halal", "Healthy Option", "Vegetarian", "Vegan", "Gluten Friendly", "Allergen-Friendly", "Vegan Option Available"]

            # adding nutritional information
            for info in base_nutritional:
                existing_info = Nutritional_Information.query.filter_by(info=info).first()
                if not existing_info:
                    new_info = Nutritional_Information(info=info)
                    db.session.add(new_info)

            db.session.commit()

            base_restrictions = ["Gluten/Wheat", "Milk", "Eggs", "Soy", "Sesame", "Pork", "Peanuts", "Fish", "Tree Nuts", "Coconut"]

            # adding dietary restrictions
            for restriction in base_restrictions:
                existing_restriction = Dietary_Restriction.query.filter_by(restriction=restriction).first()
                if not existing_restriction:
                    new_restriction = Dietary_Restriction(restriction=restriction)
                    db.session.add(new_restriction)

            db.session.commit()

            # MEAL FOR TESTING PURPOSES
            existing_meal = Meal.query.filter_by(id=1).first()

            if (existing_meal):
                print("Temp meals exists")

            else:
                meals_test = {
                    "Lemon Poppy Seed Muffin": {"price": 8.88, "number_sold": 88, "types":"Breakfast", "category":"Bakery", "nutritional":"Vegetarian", "restriction":"Eggs,Gluten/Wheat,Milk"},
                    "Double Chocolate Chip Muffin": {"price": 8.88, "number_sold": 88, "types":"Breakfast", "category":"Bakery", "nutritional":"Vegetarian", "restriction":"Eggs,Gluten/Wheat,Milk,Soy"},
                    "Mini Apple Spice Bread Loaf": {"price": 8.88, "number_sold": 88, "types":"Breakfast", "category":"Bakery", "nutritional":"Halal,Vegan,Vegetarian", "restriction":"Gluten/Wheat"},
                    "Blueberry Cream Sweet Bread": {"price": 8.88, "number_sold": 88, "types":"Breakfast", "category":"Bakery", "nutritional":"Halal,Vegetarian", "restriction":"Eggs,Gluten/Wheat,Milk,Soy"},
                    "Jelly Swirl Coffee Cake": {"price": 8.88, "number_sold": 88, "types":"Breakfast", "category":"Bakery", "nutritional":"Halal,Vegetarian", "restriction":"Eggs,Gluten/Wheat,Milk,Soy"},
                    "Coug Breakfast Sandwich w/ Cheese": {"price": 8.88, "number_sold": 88, "types":"Breakfast", "category":"Build-a-Breakfast Sandwich", "nutritional":"Halal,Vegetarian", "restriction":"Eggs,Gluten/Wheat,Milk,Soy"},
                    "Coug Breakfast Sandwich w/ Bacon": {"price": 8.88, "number_sold": 88, "types":"Breakfast", "category":"Build-a-Breakfast Sandwich", "nutritional":"Halal,Vegetarian", "restriction":"Eggs,Gluten/Wheat,Milk,Pork,Soy"},
                    "Southwest Tofu Scramble w/ Daiya Cheese": {"price": 8.88, "number_sold": 88, "types":"Breakfast", "category":"Chef's Creation", "nutritional":"Gluten Friendly,Halal,Healthy Option,Vegan,Vegetarian", "restriction":"Soy"},
                    "Oatmeal": {"price": 8.88, "number_sold": 88, "types":"Breakfast", "category":"Hot Cereal", "nutritional":"Halal,Healthy Option,Vegan,Vegetarian", "restriction":"Gluten/Wheat"},
                    "Coconut BLT Sandwich": {"price": 8.88, "number_sold": 88, "types":"Lunch", "category":"Chef's Creation", "nutritional":"Halal,Vegan,Vegetarian", "restriction":"Coconut,Gluten/Wheat,Soy"},
                    "Grasshopper Bar": {"price": 8.88, "number_sold": 88, "types":"Lunch,Dinner", "category":"Bakery", "nutritional":"Vegetarian", "restriction":"Eggs,Gluten/Wheat,Milk,Soy"},
                    "Gardein Black Bean Burger": {"price": 8.88, "number_sold": 88, "types":"Lunch,Dinner", "category":"Big Cat Grille", "nutritional":"Halal,Vegan,Vegetarian", "restriction":"Gluten/Wheat,Sesame,Soy"},
                    "NS Par Stock Deli": {"price": 8.88, "number_sold": 88, "types":"Lunch,Dinner", "category":"Deli", "nutritional":"", "restriction":"Eggs,Gluten/Wheat,Milk,Soy"},
                    "Chile Margarita Chicken": {"price": 8.88, "number_sold": 88, "types":"Lunch,Dinner", "category":"Natural", "nutritional":"Allergen-Friendly,Gluten Friendly", "restriction":""},
                    "Build Your Own Sandwich": {"price": 8.88, "number_sold": 88, "types":"Lunch", "category":"Presto Pizza", "nutritional":"Vegan Option Available", "restriction":"Eggs,Gluten/Wheat,Milk"},
                    "NS Yogurt Bar": {"price": 8.88, "number_sold": 88, "types":"Lunch,Dinner", "category":"Salads", "nutritional":"", "restriction":"Eggs,Gluten/Wheat,Milk,Soy"},
                    "Tomato Basil Soup": {"price": 8.88, "number_sold": 88, "types":"Lunch,Dinner", "category":"Soups", "nutritional":"Gluten Friendly,Halal,Vegetarian", "restriction":"Milk"},
                    "Quick Kimchi": {"price": 8.88, "number_sold": 88, "types":"Dinner", "category":"Chef's Creation", "nutritional":"Allergen-Friendly,Gluten-Friendly,Halal,Healthy Option,Vegan,Vegetarian", "restriction":""}
                }

                # adding meals - unpacking nested dictionary
                for name, data in meals_test.items():

                    new_meal = Meal(
                        meal_name = name,
                        price = data["price"],
                        number_sold = data["number_sold"]
                    )

                    # updating relationship with categories
                    temp_category = Meal_Category.query.filter_by(category=data["category"]).first()
                    new_meal.categories.append(temp_category)

                    # updating nutritional information (ex: vegetarian)
                    for info in data["nutritional"].split(","):
                        temp_info = Nutritional_Information.query.filter_by(info=info).first()
                        if not temp_info:
                            break
                        else:
                            new_meal.infos.append(temp_info)
                        
                    # updating restrictions information (ex: allergens)
                    for restriction in data["restriction"].split(","):
                        temp_restriction = Dietary_Restriction.query.filter_by(restriction=restriction).first()
                        if not temp_restriction:
                            break
                        else:
                            new_meal.restrictions.append(temp_restriction)

                    # updating types
                    for type in data["types"].split(","):
                        temp_type = Meal_Type.query.filter_by(type=type).first()
                        if not temp_type:
                            break
                        else:
                            new_meal.types.append(temp_type)

                    db.session.add(new_meal)

                db.session.commit()        

            # TEMP MENU FOR TESTING PURPOSES (since no info in database yet)
            existing_menu = Menu.query.filter_by(id=1).first()
            
            if (existing_menu):
                print("Temp menu exists")

            else:
                
                temp_menu = Menu(
                    date = date(2025, 4, 2),
                    location = "Northside"
                )

                # updating relationship; adding categories to menu
                for category in Meal_Category.query.all():
                    temp_menu.meal_categories.append(category)

                # add temp meal
                for meal in Meal.query.all():
                    temp_menu.meals.append(meal)

                db.session.add(temp_menu)
                db.session.commit()
        
### Program entrypoint (place at bottom of script)
#create_db() ## Create all databasees if they don't exist

# above is incorrect - you only create a db if it doesnt exist
if not os.path.exists(os.path.join(basedir, "data/database.db")):
    create_db()


# Initialize bcrypt
bcrypt.init_app(app)

# Flask login setup
login_manager = LoginManager()
login_manager.login_view = 'views.login'
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    print(f"Redirecting to login: {url_for(login_manager.login_view, next=request.url)}")
    return redirect(url_for(login_manager.login_view, next=request.url))

## FROM ADMIN PORTAL MERGE CONFLICT BRANCH, DELETE IF NOT NEEDED.
# choose meal plan (with id)
@app.route("/<int:student_id>/meal-plan", methods=["GET", "POST"])
def meal_plan_id(student_id):

    # find student in database
    student = Student.query.filter_by(user_id=student_id).first()
    
    # display error & return to home if student not found
    if not student:
        print("Student does not exist")
        return "<h3>Student does not exist!</h3>" \
        "<form action='/'><button type='submit'>Return Home</button></form>"
    
    # updating meal plan
    if request.method == 'POST':
        print("Now changing meal plan")
        updated_plan = request.form.get("plan_id")
        student.plan_id = int(updated_plan)
        db.session.commit() # update in database
        # BASE TYPES FOR TESTING
        base_types = ["Breakfast", "Lunch", "Brunch", "Dinner"]
        for type in base_types:
            existing_type = Meal_Type.query.filter_by(type=type).first()
            if not existing_type:
                new_type = Meal_Type(type=type)
                db.session.add(new_type)
            
        db.session.commit()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True) #debugg

