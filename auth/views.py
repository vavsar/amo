import json
import os

import requests

AMO_SECRET_KEY = 'c5k6Y0oDTImLBttZefrJq1NFInK0r6pWiPzCeUKeiZzURAnw7mIHAPXUXlzpg8sq'
AMO_ID_INTEGRATION = '7d0b40b1-f8a2-4b88-b935-b43471e2f485'
REDIRECT_URL_NGROK = "http://3e69-5-167-144-64.ngrok.io/"
REDIRECT_URL_BASE = REDIRECT_URL_NGROK + "app/get_key/"
ACCESS_TOKEN = os.getenv("access_token")
REFRESH_TOKEN = os.getenv("refresh_token")
EXPIRES_IN = os.getenv("expires_in")
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}


def get_key_view(request):
    code = request.GET.get('code')
    return code


def get_first_token(request, grant_type):
    code = get_key_view(request)
    headers = {
        "Content-Type": "application/json",
    }
    new_data = {
        "client_id": AMO_ID_INTEGRATION,
        "client_secret": AMO_SECRET_KEY,
        "grant_type": grant_type,
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
    with open('.env', 'w') as f:
        f.write('access_token = ' + access_token + '\n')
        f.write('refresh_token = ' + refresh_token + '\n')
        f.write('expires_in = ' + str(expires_in))


def get_token(request):
    get_first_token(request, "authorization_code")
