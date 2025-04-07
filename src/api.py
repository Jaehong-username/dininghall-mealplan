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
        
        
        # look for table and return data.
        table = tables_dict[table_id]
        if table is not None:
            results = table.query.all()
            return jsonify([table_item.to_dict() for table_item in results])
        else:
            print("Could not find table " + table_id + "!")
    else:
        if(current_user.is_admin() == False):
            return jsonify({'error': 'Unauthorized request'}), 403
        elif table_id is None:
            return jsonify({'error': 'table_id not supplied'}), 404
        else:
            return jsonify({'error': 'Error retrieving data'}), 404
    return jsonify({'error': 'Unauthorized request'}), 403
    
    
@api_bp.route("/api/delete_user", methods=["GET", "POST"])
def delete_entry():
    # Get user id
    key = request.form.get("id")
    if(current_user.is_admin() and key is not None):
        user = User.query.get(int(key))
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        else:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'success': 'User deleted.'}), 200
    else:
        return jsonify({'error': 'Unauthorized request'}), 403
    pass
# TODO: Implement API endpoint for adding, deleting, and editing database items via the inline forms on the dashboard.