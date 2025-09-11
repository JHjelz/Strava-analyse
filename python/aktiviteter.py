# STRAVA-ANALYSE/python/aktiviteter.py

# Bibliotek

import requests

# Funksjoner

def hent_aktiviteter(access_token, per_page=5):
    """
    Henter aktiviteter fra Strava.
    """
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, params={"per_page": per_page})
    response.raise_for_status()
    return response.json()
