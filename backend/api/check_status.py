import re

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from psycopg2 import sql

from app.models import check_auth, authorize, config
from pay import check_farmer, update_farmer
from database import Database

check_status_bp = Blueprint('check_status', __name__)


@check_status_bp.route('/check_status', methods=['GET'])
def check_status():
    """Status"""
    vozvrat = {}
    user = check_auth(request.headers, __name__)
    if user != True:
        return user
    user = authorize.get(request.headers.get('UserToken'))
    try:
        database = Database(config)
    except TypeError:
        vozvrat["messageError"] = "Нет подключения к БД"
        return jsonify(vozvrat)

    query = sql.SQL("SELECT fns_id FROM public.user_fns WHERE user_id="+str(user.get_id()))
    try:
        query_id = database.select_data(query)[0]
    except:
        vozvrat["messageError"] = "Данной заявки нет"
        return jsonify(vozvrat)
    # inn = str(user.get_inn())

    if check_farmer().get("payload").get("result") == "COMPLETED":
        vozvrat["result"] = "Заявка успешно подтверждена"
    else:
        vozvrat["messageError"] = "Заявка не подтверждена"
    return jsonify(vozvrat)