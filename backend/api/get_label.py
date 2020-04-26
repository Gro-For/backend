from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from psycopg2 import sql

from app.models import check_auth, authorize, config
from database import Database

get_label_bp = Blueprint('get_label', __name__)


@get_label_bp.route('/get_label', methods=['GET'])
def get_label():
    """Add product in favorite for user"""

    if request.headers.get('Token') != str(config['FLASK_APP']['SECRET_KEY']):
        return jsonify({'message': 'Не верный токен'}), 401, {'ContentType': 'application/json'}

    vozvrat = {}
    try:
        database = Database(config)
    except TypeError:
        vozvrat["messageError"] = "Нет подключения к БД"
        return jsonify(vozvrat)

    fields = [
        "u.firstname",
        "u.lastname",
        "up.id",
        "up.name",
        "up.photo",
        "up.type",
        "up.method",
        "up.sale",
        "up.price",
        "c.name",
        "up.weight",
        "u2.name",
        "a.country",
        "a.city",
        "a.address",
        "a.lat",
        "a.lng"
    ]

    query = sql.SQL("SELECT {} FROM users u \
        RIGHT JOIN users_product up on u.id = up.user_id\
        LEFT JOIN units u2 on up.unit_id = u2.id\
        LEFT JOIN currencys c on up.currency_id = c.id\
        LEFT JOIN address a on u.id = a.user_id").format(
        sql.SQL(",").join(sql.Identifier(
            i.split('.')[0], i.split('.')[1]) for i in fields)
    )

    execute = database.select_data(query)
    if type(execute) != list:
        return execute

    vozvrat = []
    for row in execute:
        data_append = {}
        for i in range(len(fields)):
            value = row[i]
            if fields[i] == "up.id":
                fields[i] = "up.users_product_id"
            if fields[i] == "c.name":
                fields[i] = "c.currency"
            if fields[i] == "u2.name":
                fields[i] = "u2.unit"

            data_append[fields[i].split('.')[1]] = value
        vozvrat.append(data_append)

    return jsonify(vozvrat)
