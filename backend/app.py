# backend/app.py

from flask import Flask, jsonify, request
import requests

from private import CLIENT_ID, CLIENT_SECRET, AUTHORIZATION_CODE

app = Flask(__name__)

# Hjelpefunksjoner:

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
        print("Feil under oppdatering av access_token:", e)
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
        response_data = response.json()
        return response_data['access_token'], response_data['refresh_token']
    except requests.exceptions.RequestException as e:
        print("Feil ved henting av access token:", e)
        return None, None

def get_all_activities(access_token, activities_per_page=100):
    """Henter alle tilgjengelige aktiviteter ved å iterere over alle sider med resultater.

    Args:
        access_token (str): Strava tilgangstoken.
        activities_per_page (int): Antall aktiviteter per side (default er 100, Stravas maksgrense).

    Returns:
        list: En liste med alle aktiviteter som er hentet.
    """
    headers = {'Authorization': f'Bearer {access_token}'}
    all_activities = []
    page = 1
    
    while True:
        response = requests.get(
            'https://www.strava.com/api/v3/athlete/activities',
            headers=headers,
            params={'page': page, 'per_page': activities_per_page}
        )
        
        if response.status_code != 200:
            print(f"Feil ved henting av data på side {page}: {response.status_code}")
            break
        
        activities = response.json()
        if not activities:
            break
        
        all_activities.extend(activities)
        page += 1
    
    if len(all_activities) == 0:
        return None
    return all_activities

@app.route('/get_strava_data', methods=['POST'])
def get_strava_data():
    data = request.get_json()
    client_id = data.get('client_id')
    client_secret = data.get('client_secret')
    authorization_code = data.get('authorization_code')

    # Hent eller oppdater tokens
    access_token, refresh = get_access_token(client_id, client_secret, authorization_code)

    if not access_token:
        return jsonify({"error": "Kunne ikke hente access token"}), 400

    activities = get_all_activities(access_token)

    if activities:
        return jsonify(activities)
    else:
        return jsonify({"error": "Kunne ikke hente data fra Strava"}), 500

if __name__ == '__main__':
    app.run(debug=True)
