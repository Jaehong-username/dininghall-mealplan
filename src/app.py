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
                balance=1000.00
            )

            db.session.add(temp_student)
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