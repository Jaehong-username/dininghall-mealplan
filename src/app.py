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
create_db() ## Create all databasees if they don't exist

### -- Routes -- ###
@app.route("/")
def index():
    return render_template("index.html")

### Program entrypoint (place at bottom of script)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)