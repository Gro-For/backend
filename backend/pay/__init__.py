import requests
import uuid

from app.models import config


def auth_fns():
    data = {
        "username": config['FNS']['USERNAME'],
        "password": config['FNS']['PASSWORD'],
        "grant_type": config['FNS']['GRANT_TYPE'],
        "client_id": config['FNS']['CLIENT_ID']
    }
    url = 'https://ktir.smz.w1.money/api/token/'
    response = requests.post(url, data=data).json()
    access_token = response["access_token"]
    return access_token


def add_new_farmer_to_fns(inn):
    token = auth_fns()
    guid = str(uuid.uuid4())
    url = "https://ktir.smz.w1.money/api/smz/postBindPartnerWithInnRequest?externalId=" + guid
    headers = {"Authorization": "Bearer %s" % token}
    data = {
        "inn": inn,
        "permissions": [
            "INCOME_REGISTRATION",
            "PAYMENT_INFORMATION",
            "INCOME_LIST",
            "INCOME_SUMMARY",
            "CANCEL_INCOME",
            "CANCEL_ANY_INCOME"
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    result = get_result(guid, token)
    while result.get("state") == "Pending":
        result = get_result(guid, token)
    if result.get('payload').get('message') != None:
        vozvrat = result["payload"]["message"]
    elif result.get("payload").get("id"):
        vozvrat = int(result.get("payload").get("id"))
    else:
        vozvrat = "Result failed"
    return vozvrat


def check_farmer(query_id):
    token = auth_fns()
    guid = str(uuid.uuid4())
    url = "https://ktir.smz.w1.money/api/smz/getBindPartnerStatusRequest?externalId=" + guid
    headers = {"Authorization": "Bearer %s" % token}
    data = {
        "id": query_id,
    }
    response = requests.post(url, json=data, headers=headers)
    result = get_result(guid, token)
    print(result)
    if result.get("state") == "Failed":
        vozvrat = "Result failed"
    else:
        vozvrat = result
    return vozvrat


def update_farmer(inn):
    token = auth_fns()
    guid = str(uuid.uuid4())
    url = "https://ktir.smz.w1.money/api/smz/getTaxpayerStatusRequest?externalId=" + guid
    headers = {"Authorization": "Bearer %s" % token}
    data = {
        "inn": inn,
    }
    response = requests.post(url, json=data, headers=headers)
    result = get_result(guid, token)
    print(result)
    if result["state"] == "Failed":
        vozvrat = "Result failed"
    else:
        vozvrat = result
    return vozvrat


def get_result(guid, token):
    token = auth_fns()
    url = "https://ktir.smz.w1.money/api/smz/getResponse?externalId=" + guid
    headers = {"Authorization": "Bearer %s" % token}
    response = requests.get(url, headers=headers).json()
    return response


def valid_farmer_inn(user):
    token = auth_fns()
    guid = str(uuid.uuid4())
    url = "https://ktir.smz.w1.money/api/smz/getInnByPersonalInfoRequest?externalId=" + guid
    headers = {"Authorization": "Bearer %s" % token}
    print(user['birthday'])
    data = {
        "birthday": str(user['birthday']),
        "firstName": user['firstname'],
        "passportNumber": user['number_passport'],
        "passportSeries": user['serial_passport'],
        "secondName": user['lastname'],
        "patronymic": user['patronymic'],
        "inn": user['inn']
    }
    response = requests.post(url, json=data, headers=headers)
    result = get_result(guid, token)
    while result["state"] == "Pending":
        result = get_result(guid, token)
    print(result)
    if result.get("state") == "Failed":
        vozvrat = "Result failed"
    else:
        if result.get('payload').get('message') != None:
            vozvrat = result["payload"]["message"]
        else:
            vozvrat = result["payload"]["status"]
        if vozvrat == "TAXPAYER_NOT_FOUND":
            vozvrat = "Налогоплательщик не найден в системе ФНС"
    return vozvrat
