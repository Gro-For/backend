from flask import request, Blueprint, jsonify

from database import Database
from app.models import config

api_bp = Blueprint('api', __name__)


@api_bp.route('/api', methods=['GET', 'POST'])
def api():
    database = Database(config)
    if database != True:
        return jsonify({"messageError": database})
    if request.method == 'POST':
        body = request.get_json()
        if body["type"] == "registration":
            pass
        return 'ok'
    else:
        return jsonify({"message": database.query("SELECT * FROM users")})


POST = {  # registration
    "type": "registration",
    "first_name": "",
    "last_name": "",
    "father_name": "",  # необязательно
}
