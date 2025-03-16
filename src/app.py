#flask library packages
from flask import *
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
# Flask forms extension packages
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
# System packages
from pathlib import Path
import os
import secrets
from models import *
# Form definitions script
from form_classes import *

app = Flask(__name__) # Create flask application

### -- Initialization, configuration -- ###
# Database file location
# Using SQLite for now since it's portable and easy to set up.
basedir = os.path.abspath(os.path.dirname(__file__))

# Create secret key
secret = secrets.token_urlsafe(16)
app.secret_key = secret

# Enable Flask-Wtforms CSRF protection
csrf = CSRFProtect(app)

# Initialize bcrypt
bcrypt.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "data/database.db")
db.init_app(app)

# Flask login setup
login_mgr = LoginManager()
@login_mgr.user_loader
def load_user(id):
    return User.query.get(int(id))
login_mgr.init_app(app)

# Create all databases if they don't exist
def create_db():
    with app.app_context():
        db.create_all()
create_db() 

### -- Routes -- ###
@app.route("/", methods=['GET','POST'])
def index():
    return render_template("index.html")

# Test page to implement basic account registration
@app.route("/register_test", methods=['GET', 'POST'])
def register_test():
    form = RegisterForm()
    message = ""
    if form.validate_on_submit():
        # If form submitted
        new_user = User(form.email.data, form.name.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()
        
        # Try adding a new student with that account
        student = Student(new_user.user_id, 12345)
        db.session.add(student)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template("register_test.html", form=form)

# Test page to implement basic account login
@app.route("/login_test", methods=['GET', 'POST'])
def login_test():
    form = LoginForm()
    message = ""
    if form.validate_on_submit():
        # If form submitted
        user = User.test_login(form.email.data, form.password.data)
        
        if(user is not None):
            login_user(user)
            return redirect(url_for('index'))
        else:
            message = "ERROR: Invalid username or password!"
    return render_template("login_test.html", message=message, form=form)

@app.route("/log-out", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route("/account", methods=['GET','POST'])
def account_page():
    if(current_user.is_authenticated):
        current_student = Student.query.filter_by(user_id=current_user.user_id).first()
        if(current_student is not None):
            return render_template("student_info.html", balance=current_student.balance)
    return redirect(url_for('index'))

### Program entrypoint (place at bottom of script)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)