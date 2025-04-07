from flask import *
from flask_login import *
from json import *
from models import *

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/api/get_admin_data', methods=['GET', 'POST'])
@login_required
def get_admin_data():
    table_id = request.form.get("table_id")
    if(current_user.is_admin() and table_id is not None):
        # populate table dictionary
        tables_dict = {}
        for table in db.Model.__subclasses__():
            tables_dict[table.__tablename__] = table
        
        print("Attempting to get table " + table_id)
        
        # look for table and return data.
        table = tables_dict[table_id]
        if table is not None:
            print("Table found!")
            results = table.query.all()
            return jsonify([table_item.to_dict() for table_item in results])
        else:
            print("Could not find table " + table_id + "!")
    else:
        if(current_user.is_admin() == False):
            print("User is not admin!")
        elif table_id is None:
            print("table_id not supplied!")
        else:
            print("Error retrieving data.")
    abort(403)
    
    
@api_bp.route("/api/delete_user", methods=["GET", "POST"])
def delete_entry():
    # Get user id
    key = request.form.get("id")
    
    pass
# TODO: Implement API endpoint for adding, deleting, and editing database items via the inline forms on the dashboard.