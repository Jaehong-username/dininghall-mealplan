#flask library packages
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
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
from datetime import date

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "data/database.db")
bcrypt = Bcrypt(app)

# Create secret key
secret = secrets.token_urlsafe(16)
app.config['SECRET_KEY'] = secret
csrf = CSRFProtect(app)

app.register_blueprint(views)
app.register_blueprint(models_bp)

# Create all databases if they don't exist
db.init_app(app)

def create_db():
    with app.app_context():
        db.create_all()
        
        # TEMP STUDENT FOR TESTING PURPOSES (since no info in database yet)
        existing_user = User.query.filter_by(user_id=1).first()

        if (existing_user):
            print("Temp user exists")
        
        else:
            temp_user = User(
                name="test",
                email="test@email.com",
                password="test"
            )

            db.session.add(temp_user)
            db.session.commit()

            temp_student = Student(
                user_id=temp_user.user_id,
                balance=1000.00
            )

            db.session.add(temp_student)
            db.session.commit()

        # TEMP MEAL CATEGORIES FOR TESTING PURPOSES (based on wsu)
        base_categories = ["Bakery", "Build-a-Breakfast-Sandwich", "Chef's Creation", "Hot Cereal",
                           "Big Cat Grille", "Deli", "Natural", "Presto Pizza", "Salads", "Soups"]

        # adding categories to meal_category
        for category in base_categories:
            existing_category = Meal_Category.query.filter_by(category=category).first()
            if not existing_category:
                new_category = Meal_Category(category=category)
                db.session.add(new_category)

        db.session.commit()

         # TEMP MEAL ATTRIBUTES FOR TESTING PURPOSES
        base_nutritional = ["Halal", "Healthy Option", "Vegetarian", "Vegan", "Gluten Friendly", "Allergen-Friendly"]

        # adding nutritional information
        for info in base_nutritional:
            existing_info = Nutritional_Information.query.filter_by(info=info).first()
            if not existing_info:
                new_info = Nutritional_Information(info=info)
                db.session.add(new_info)

        base_restrictions = ["Gluten/Wheat", "Milk", "Eggs", "Soy", "Sesame", "Pork", "Peanuts", "Fish", "Tree Nuts", "Coconut"]

        # adding dietary restrictions
        for restriction in base_restrictions:
            existing_restriction = Dietary_Restriction.query.filter_by(restriction=restriction).first()
            if not existing_restriction:
                new_restriction = Dietary_Restriction(restriction=restriction)
                db.session.add(new_restriction)

        db.session.commit()

        # TEMP MEAL FOR TESTING PURPOSES
        existing_meal = Meal.query.filter_by(meal_id=1).first()

        if (existing_meal):
            print("Temp meals exists")

        else:
            temp_meal = Meal(
                meal_name="Starfruit Smoothie",
                price = 8.88,
                number_sold = 88,
                type = "Breakfast"
            )

            breakfast_bakery1 = Meal(
                meal_name="Lemon Poppy Seed Muffin",
                price = 8.88,
                number_sold = 88,
                type = "Breakfast"
            )

            breakfast_bakery2 = Meal(
                meal_name="Double Chocolate Chip Muffin",
                price = 8.88,
                number_sold = 88,
                type = "Lunch"
            )

            breakfast_sandwich = Meal(
                meal_name="Coug Breakfast Sandwich w/ Cheese",
                price = 8.88,
                number_sold = 88,
                type = "Breakfast"
            )

            # adding meal attributes
            for info in Nutritional_Information.query.all():
                temp_meal.infos.append(info)
                breakfast_bakery1.infos.append(info)
                breakfast_bakery2.infos.append(info)
                breakfast_sandwich.infos.append(info)

            # adding meal attributes
            for restriction in Dietary_Restriction.query.all():
                temp_meal.restrictions.append(restriction)
                breakfast_bakery1.restrictions.append(restriction)
                breakfast_bakery2.restrictions.append(restriction)
                breakfast_sandwich.restrictions.append(restriction)

            # relationships updating for categories
            temp_meal.categories.append(Meal_Category.query.filter_by(category="Natural").first())
            breakfast_bakery1.categories.append(Meal_Category.query.filter_by(category="Bakery").first())
            breakfast_bakery2.categories.append(Meal_Category.query.filter_by(category="Bakery").first())
            breakfast_sandwich.categories.append(Meal_Category.query.filter_by(category="Build-a-Breakfast-Sandwich").first())

            db.session.add(temp_meal)
            db.session.add(breakfast_bakery1)
            db.session.add(breakfast_bakery2)
            db.session.add(breakfast_sandwich)

            db.session.commit()        

        # TEMP MENU FOR TESTING PURPOSES (since no info in database yet)
        existing_menu = Menu.query.filter_by(date=date(2025, 4, 2)).first()
        
        if (existing_menu):
            print("Temp menu exists")

        else:
            temp_menu = Menu(
                date = date(2025, 4, 2),
                location = "Northside Cafe"
            )

            # updating relationship
            for category in Meal_Category.query.all():
                temp_menu.meal_categories.append(category)

            # add temp meal
            temp_menu.meals.append(temp_meal)
            temp_menu.meals.append(breakfast_bakery1)
            temp_menu.meals.append(breakfast_bakery2)
            temp_menu.meals.append(breakfast_sandwich)

            db.session.add(temp_menu)
            db.session.commit()
        
### Program entrypoint (place at bottom of script)
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)