# STRAVA-ANALYSE/python/tilgang.py

# Bibliotek:

import requests
import time

from privat import privat_info

# Funksjoner:

"""
Om ACCESS_TOKEN utløper, kjør denne koden.
Oppdater refresh_token her og der det trengs andre steder for å få applikasjonen til å fungere.
Oppdater access_token der det trengs andre steder for å få applikasjonen til å fungere.
"""

def oppdater_access_token(client_id, client_secret, refresh_token):
    """
    Henter ny access token og refresh token fra Strava.
    """
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
        return response_data['access_token'], response_data['refresh_token'], response_data['expires_at']
    except requests.exceptions.RequestException as e:
        print(f"Feil under oppdatering av access_token: {e}")
        return None, None, None

"""
Dette er funksjonen for  å starte oppsettet. Målet er å få tak i AUTHORIZATION_CODE.

Bruk følgende lenke i nettleseren din med den gitte client_id:
https://www.strava.com/oauth/authorize?client_id=ID&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=read_all,activity:read_all

Du vil da komme til en side hvor du trykker 'Authorize'.
Du kommer så til en side som ikke eksisterer med lenke lik den under:
http://localhost/?state=&code=authCode&scope=read,activity:read_all,read_all

Her må du kopiere AUTHORIZATION_CODE.
"""

def fa_access_token(client_id, client_secret, authorization_code):
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
        return response_data['access_token'], response_data['refresh_token'], response_data['expires_at']
    except requests.exceptions.RequestException as e:
        print(f"Feil under oppdatering av access_token: {e}")
        return None, None, None

def sikre_tokens(info: privat_info):
    """
    Sørger for at tokens er gyldige.
    Hvis strava_tokens.json ikke finnes - bruk authorization_code for første init.
    Ellers - bruk refresh_token for å fornye access token.
    """
    kreditering = info.fa_private_info()
    client_id = kreditering["client_id"]
    client_secret = kreditering["client_secret"]
    access_token = kreditering.get("access_token")
    refresh_token = kreditering.get("refresh_token")
    expires_at = kreditering.get("expires_at", 0)

    now = int(time.time())

    if not access_token or not refresh_token:
        print("Ingen tokens funnet, henter nye med authorization_code...")
        access_token, refresh_token, expires_at = fa_access_token(
            client_id, client_secret, kreditering["authorization_code"]
        )
        info.lagre_tokens(access_token, refresh_token, expires_at)
    elif now >= expires_at:
        print("Access_token er utløpt, oppdaterer tokens med refresh_token...")
        new_access_token, new_refresh_token, new_expires_at = oppdater_access_token(
            client_id, client_secret, refresh_token
        )
        if new_access_token:
            access_token, refresh_token, expires_at = new_access_token, new_refresh_token, new_expires_at
            info.lagre_tokens(access_token, refresh_token, expires_at)
    else:
        print(f"Access token er fortsatt gyldig i {expires_at - now} sekunder.")
    return access_token, refresh_token
