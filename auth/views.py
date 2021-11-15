import json
import os
import requests
from django.http import HttpResponse

from dotenv import load_dotenv

load_dotenv()

AMO_SECRET_KEY = os.getenv("AMO_SECRET_KEY")
AMO_ID_INTEGRATION = os.getenv("AMO_ID_INTEGRATION")
ACCESS_TOKEN = os.getenv("access_token")
REFRESH_TOKEN = os.getenv("refresh_token")
EXPIRES_IN = os.getenv("expires_in")
REDIRECT_URL_NGROK = "http://3e69-5-167-144-64.ngrok.io/"
REDIRECT_URL_BASE = REDIRECT_URL_NGROK + "app/get_key/"


def get_key_view(request):
    code = request.GET.get('code')
    return code


def get_first_token(request):
    code = get_key_view(request)
    headers = {
        "Content-Type": "application/json",
    }
    new_data = {
        "client_id": AMO_ID_INTEGRATION,
        "client_secret": AMO_SECRET_KEY,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URL_BASE
    }
    data = json.dumps(new_data)
    response = requests.post(
        'https://ncy61970.amocrm.ru/oauth2/access_token',
        headers=headers,
        data=data
    ).json()
    access_token = response['access_token']
    refresh_token = response['refresh_token']
    expires_in = response['expires_in']
    with open('.env', 'a') as f:
        f.write('access_token = ' + access_token + '\n')
        f.write('refresh_token = ' + refresh_token + '\n')
        f.write('expires_in = ' + str(expires_in))
    return HttpResponse('Token is got')
