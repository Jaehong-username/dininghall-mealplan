from flask import Flask, render_template, request, url_for, make_response, redirect, jsonify
from flask_login import LoginManager
from pathlib import Path
import os

# Database definition script
from models import *

app = Flask(__name__) # Create flask application

### Initialization, configuration
# Database file location
# Using SQLite for now since it's portable and easy to set up.
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "data/database.db")
db.init_app(app) # initialize databases
bcrypt.init_app(app) # initialize bcrypt

def create_db():
    with app.app_context():
        db.create_all()
        
        # TEMP STUDENT FOR TESTING PURPOSES (since no info in database yet)
        # to clean out (ONLY DO WITH NON-IMPORTANT DB): rm database.db & rerun code after commenting code out
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
                balance=1000.00,
                admin_id=1,
                plan_id=1
            )

            db.session.add(temp_student)
            db.session.commit()

create_db() ## Create all databasees if they don't exist

### -- Routes -- ###
@app.route("/")
def index():
    return render_template("index.html")

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

    return render_template("meal-plan.html", student=student)

# choose meal plan (without id)
@app.route("/meal-plan")
def meal_plan():
    return render_template("meal-plan.html")

### Program entrypoint (place at bottom of script)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)