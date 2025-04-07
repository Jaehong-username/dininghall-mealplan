#flask library packages
from flask import Flask, render_template, url_for, redirect
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
app.register_blueprint(api_bp)

# Create all databases if they don't exist
db.init_app(app)

# Enable foreign key constraints for SQLite every query connection.
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def create_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
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

            db.session.add(temp_user)
            db.session.add(admin_user)
            db.session.commit()

            temp_admin = Admin(
                admin_id=admin_user.user_id
            )
            db.session.add(temp_admin)
            db.session.commit()
            
            temp_student = Student(
                user_id=temp_user.user_id,
                balance=1000.00,
                admin_id=temp_admin.admin_id,
                plan_id=None
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