# Bibliotek:

import json
import os
import requests

# Variabler:

CLIENT_ID = "138324"
CLIENT_SECRET = "33c3ac7f0d1870b77570a10a845256d295c287d5"
TOKEN_FILE = "strava_token.json"

# Funksjoner:

def load_tokens():
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, 'r') as f:
        return json.load(f)

def save_tokens(data):
    with open(TOKEN_FILE, 'w') as f:
        json.dump(data, f)

def refresh_access_token(refresh_token):
    response = requests.post(
        'https://www.strava.com/api/v3/oauth/token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
    )
    response.raise_for_status()
    data = response.json()
    save_tokens(data)
    return data['access_token']

def get_valid_access_token():
    tokens = load_tokens()
    if not tokens:
        raise Exception("Ingen tokens lagret. Kjør førstegangshenting manuelt.")
    access_token = tokens['access_token']
    # Test om token virker:
    test = requests.get(
        'https://www.strava.com/api/v3/athlete',
        headers={"Authorization": f"Bearer {access_token}"}
    )
    if test.status_code == 401:
        print("Access token utløpt. Fornyer...")
        access_token = refresh_access_token(tokens['refresh_token'])
    return access_token
