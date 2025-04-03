from flask import *
from flask_login import *
from json import *
from models import *

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/api/get_admin_data', methods=['GET', 'POST'])
@login_required
def get_admin_data():
    if(current_user.is_admin() and request.args.get("table_id") is not None):
        # populate table dictionary
        tables_dict = {}
        for table in db.Model.__subclasses__():
            tables_dict[table.__tablename__] = table
        
        print("Attempting to get table " + request.args.get("table_id"))
        
        # look for table and return data.
        table = tables_dict[request.args.get("table_id")]
        if table is not None:
            results = table.query.all()
            return jsonify([table_item.to_dict() for table_item in results])
    abort(403)