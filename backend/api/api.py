from flask import request, Blueprint, jsonify

from database import Database
from app.models import config, check_auth, authorize

api_bp = Blueprint('api', __name__)


@api_bp.route('/api', methods=['GET', 'POST'])
def api():
    user = check_auth(request.headers, __name__)
    if user != True:
        return user
    user = authorize.get(request.headers.get('UserToken'))

    try:
        database = Database(config)
    except TypeError:
        return jsonify({"message": "Нет подключения к БД"})

    if request.method == 'POST':
        return 'ok'
    elif request.method == 'GET':
        return jsonify({"message": database.select_data("SELECT * FROM public.users")})


POST = {  # registration
    "type": "registration",
    "first_name": "",
    "last_name": "",
    "father_name": "",  # необязательно
}
