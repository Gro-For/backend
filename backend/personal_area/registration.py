import re

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from psycopg2 import sql

from app.models import check_auth, authorize, config
from database import Database

registration_bp = Blueprint('registration', __name__)


@registration_bp.route('/registration', methods=['GET', 'POST'])
def registration():
    """Registration new user Page"""

    user = check_auth(request.headers, __name__)
    if user != True:
        return user
    user = authorize.get(request.headers.get('UserToken'))

    vozvrat = {}
    try:
        database = Database(config)
    except TypeError:
        vozvrat["messageError"] = "Нет подключения к БД"
        return jsonify(vozvrat)

    file = request.get_json(silent=True)
    if file != None and request.method == "POST":
        user = {
            "email": file["email"] if file["email"] else None,
            "password": file["password"] if file["password"] else None,
            "confirm_password": file["confirm_password"] if file["confirm_password"] else None,
            "firstname": file["firstname"] if file["firstname"] else None,
            "lastname": file["lastname"] if file["lastname"] else None,
            "patronymic": file["patronymic"] if file["patronymic"] else None,
            "number_phone": file["number_phone"] if file["number_phone"] else None
        }
        # Проверка введённых данных
        valid = valid_data(user)
        if valid != True:
            vozvrat["messageError"] = valid
            return jsonify(vozvrat)

        user['password'] = generate_password_hash(
            user['password'], method='sha256')
        result = execute_to_base(database, user)

        if result == True:
            vozvrat["messageSuccess"] = "Пользователь зарегестрирован"
        else:
            vozvrat["messageError"] = result
    else:
        vozvrat["messageError"] = "JSON отсутсвует"
    return jsonify(vozvrat)


def execute_to_base(database, user):
    values_data = {}
    columns = {}
    for col in user:
        if col != "confirm_password":
            columns[col] = sql.Identifier(col)
            values_data[col] = sql.Literal(user[col])

    query = sql.SQL("INSERT INTO {table}({column}) VALUES({value})").format(
        table=sql.Identifier("public", "users"),
        column=sql.SQL(',').join(
            columns[col] for col in columns),
        value=sql.SQL(',').join(
            values_data[val] for val in values_data),
    )
    vozvrat = database.insert_data(query)

    return vozvrat


def valid_data(user):
    """Checking user data"""

    valid = valid_password(user['password'], user['confirm_password'])
    if valid != True:
        return valid
    valid = valid_email(user['email'], user['password'])
    if valid != True:
        return valid
    return True


def valid_email(username, password):
    """Checking username"""
    if re.search(
            "^[A-Z]{1,20}[a-z\@\.]{1,20}[\d]{0,20}[^\s\.\,\:\;\!\?\(\)\"\'\-\–]{1,20}$", username) == None:
        return "Почта не удовлетворяет требованиям"
    return True


def valid_password(password, confirm_password):
    """Checking password"""
    VALID_CHARS = [
        "[A-Z]{1,70}",
        "[a-z]{1,70}",
        "[0-9]{1,70}",
        "[\!\@\#\$\%\^\&\*\(\)\_\-\+\:\;\,\.]{0,70}"
    ]
    if password != confirm_password:
        return "Пароли не совпадают"
    for val in VALID_CHARS:
        if re.search(
                val, password) == None:
            return "Пароль не удовлетворяет требованиям"
    last_char = ""
    quantity = 0
    for char in password:
        if char != last_char:
            last_char = char
        elif char == last_char and quantity < 3:
            quantity += 1
        else:
            return "Пароль не удовлетворяет требованиям"
    return True
