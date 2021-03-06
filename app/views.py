import json
import os

import requests

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

load_dotenv()

AMO_SECRET_KEY = os.getenv("AMO_SECRET_KEY")
AMO_ID_INTEGRATION = os.getenv("AMO_ID_INTEGRATION")
ACCESS_TOKEN = os.getenv("access_token")
REFRESH_TOKEN = os.getenv("refresh_token")
EXPIRES_IN = os.getenv("expires_in")
REDIRECT_URL_NGROK = "http://3e69-5-167-144-64.ngrok.io/"
REDIRECT_URL_BASE = REDIRECT_URL_NGROK + "app/get_key/"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}


@csrf_exempt
def create_deal(request, user_id):
    new_data = [{
        "name": "Сделка для примера 1",
        "price": 20000,
        "_embedded": {
            "contacts": [
                {
                    "id": user_id
                }
            ]
        }
    }]
    data = json.dumps(new_data)
    requests.post(
        'https://ncy61970.amocrm.ru//api/v4/leads',
        data=data,
        headers=HEADERS,
    )


def get_contact(request):
    name = request.GET.get('name', '')
    email = request.GET.get('email', '')
    phone = request.GET.get('phone', '')
    new_data = [{
        "name": f"{name}",
        "custom_fields_values": [
            {
                "field_id": 570821,
                "field_name": "Телефон",
                "values": [
                    {
                        "value": f"{phone}",
                        "enum_code": "MOB"
                    }
                ]
            },
            {
                "field_id": 570823,
                "field_name": "Email",
                "values": [
                    {
                        "value": f"{email}",
                        "enum_code": "WORK"
                    }
                ]
            }
        ]
    }]
    data = json.dumps(new_data)
    if email != '':
        payload = {
            "query": f"{email}",
        }
    elif phone != '':
        payload = {
            "query": f"{phone}",
        }
    else:
        payload = {
            "query": f"{name}",
        }

    response = requests.get(
        'https://ncy61970.amocrm.ru//api/v4/contacts',
        params=payload,
        headers=HEADERS
    )
    try:
        r = response.json()
        user_id = r['_embedded']['contacts'][0]['id']
        requests.patch(
            'https://ncy61970.amocrm.ru//api/v4/contacts/{}'.format(user_id),
            headers=HEADERS,
            data=data
        )
        create_deal(request, user_id)
    except:
        response = requests.post(
            'https://ncy61970.amocrm.ru//api/v4/contacts',
            headers=HEADERS,
            data=data
        ).json()
        user_id = response['_embedded']['contacts'][0]['id']
        create_deal(request, user_id)
    return HttpResponse('Deal created')
