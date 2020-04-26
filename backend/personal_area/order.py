from flask import Blueprint, request, jsonify
from psycopg2 import sql

from app.models import check_auth, authorize, config
from database import Database

order_bp = Blueprint('order', __name__)


@order_bp.route('/create_order', methods=['GET', 'POST'])
def create_order():
    """Order"""
    user = check_auth(request.headers, __name__)
    if user != True:
        return user
    user = authorize.get(request.headers.get('UserToken'))

    vozvrat = {}
    database = None
    try:
        database = Database(config)
    except TypeError:
        vozvrat["messageError"] = "Нет подключения к БД"
        return jsonify(vozvrat)
    if request.method == 'GET':
        query = sql.SQL("SELECT id, name FROM {table}").format(
            table=sql.Identifier("public", "payment_methods"),
        )
        execute = database.select_data(query)
        if type(execute) != list:
            return execute

        vozvrat['payment_methods'] = {}
        for row in execute:
            vozvrat['payment_methods'][row[1]] = int(row[0])

        delivery_methods = {
            "Самовывоз": 1,
            "Доставка": 2
        }
        vozvrat['delivery_methods'] = {}
        for col in delivery_methods:
            vozvrat['delivery_methods'][col] = delivery_methods[col]
        return jsonify(vozvrat)

    file = request.get_json(silent=True)
    if file != None:
        # Получение корзины
        cart = get_cart(database, user)
        if type(cart) != list:
            return cart
        # Отправка order в базу данных
        order = {
            "user_id": user.get_id(),
            "all_price": float(database.select_data("SELECT sum(price_for_user) FROM cart WHERE user_id={}".format(user.get_id()))),
            "delivery_method_id": file.get("delivery"),
            "payment_method_id": file.get("payment_method_id"),
            "payment_status": False
        }
        result = execute_to_base(database, order)

        if result != True:
            vozvrat["messageError"] = result

        result = migrations_product_list_from_cart_in_order(database, order)
        if result == True:
            vozvrat["messageSuccess"] = "Заказ оформлен"
        else:
            vozvrat["messageError"] = result
    else:
        vozvrat["messageError"] = "JSON отсутсвует"
    return jsonify(vozvrat)


def get_cart(database, user):
    fields = [
        "id",
        "users_product_id",
        "photo",
        "farmer_price",
        "weight_user",
        "sale",
        "price_for_user"
    ]
    query = sql.SQL("SELECT {fields} FROM {table} WHERE user_id={user_id}").format(
        fields=sql.SQL(",").join(sql.Identifier(i) for i in fields),
        table=sql.Identifier("public", "cart"),
        users_id=sql.Literal(user.get_id())
    )
    vozvrat = database.select_data(query)

    return vozvrat


def execute_to_base(database, order):
    query = sql.SQL("INSERT INTO {table}(order_adding_time, {column}) VALUES(now(), {value})").format(
        table=sql.Identifier("public", "orders"),
        column=sql.SQL(',').join(
            sql.Identifier(col) for col in order),
        value=sql.SQL(',').join(sql.Literal(order[col]) for col in order)
    )
    vozvrat = database.insert_data(query)
    if vozvrat != True:
        return vozvrat

    return True


def migrations_product_list_from_cart_in_order(database, order):
    return True
