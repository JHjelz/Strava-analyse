# backend/access.py

#  Bibliotek:

import requests

from activities import get_all_activities

# Funksjoner:

"""
Om ACCESS_TOKEN utløper, kjør denne koden.
Oppdater refresh_token her og der det trengs andre steder for å få applikasjonen til å fungere.
Oppdater access_token der det trengs andre steder for å få applikasjonen til å fungere.
"""

def refresh_access_token(client_id, client_secret, refresh_token):
    """Henter ny access token og refresh token."""
    try:
        response = requests.post(
            'https://www.strava.com/api/v3/oauth/token',
            data={
                'client_id': client_id,
                'client_secret': client_secret,
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token'
            }
        )
        response.raise_for_status()  # Sjekker for HTTP-feil
        response_data = response.json()
        return response_data['access_token'], response_data['refresh_token']
    except requests.exceptions.RequestException as e:
        print(f"Feil under oppdatering av access_token: {e}")
        return None, None

"""
Dette er funksjonen for  å starte oppsettet. Målet er å få tak i AUTHORIZATION_CODE.

Bruk følgende lenke i nettleseren din med den gitte client_id:
https://www.strava.com/oauth/authorize?client_id=ID&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=read_all,activity:read_all

Du vil da komme til en side hvor du trykker 'Authorize'.
Du kommer så til en side som ikke eksisterer med lenke lik den under:
http://localhost/?state=&code=authCode&scope=read,activity:read_all,read_all

Her må du kopiere AUTHORIZATION_CODE.
"""

def get_access_token(client_id, client_secret, authorization_code):
    try:
        response = requests.post(
            'https://www.strava.com/api/v3/oauth/token',
            data={
                'client_id': client_id,
                'client_secret': client_secret,
                'code': authorization_code,
                'grant_type': 'authorization_code'
            }
        )
        response.raise_for_status()  # Sjekker for HTTP-feil
        response_data = response.json()
        return response_data['access_token'], response_data['refresh_token']
    except requests.exceptions.RequestException as e:
        print(f"Feil under oppdatering av access_token: {e}")
        return None, None

client_id = "138324"
client_secret = "33c3ac7f0d1870b77570a10a845256d295c287d5"
authorization_code = "d1ba6793d28c5228237d40670c0b407cc72b77cd"
refresh_token = "6594aa14a91dbe8e1eafb0a32058da075375330b"

print(refresh_access_token(client_id, client_secret, refresh_token))
#get_access_token(client_id, client_secret, authorization_code)