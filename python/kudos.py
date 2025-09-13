# STRAVA-ANALYSE/python/kudos.py

# Bibliotek

import requests

# Funksjoner

def hent_kudosgivere(access_token: str, aktivitet_id: int, per_page: int = 200) -> list[dict]:
    """
    Henter alle brukere som har gitt kudos på en gitt aktivitet.

    Args:
        access_token (str): Gyldig Strava access token.
        aktivitet_id (int): ID-en til aktiviteten.
        per_page (int, optional): Antall kudoers per kall (maks 200).

    Returns:
        list[dict]: Liste med atleter (brukere) som har gitt kudos.
    """
    url = f"https://www.strava.com/api/v3/activities/{aktivitet_id}/kudos"
    headers = {"Authorization": f"Bearer {access_token}"}
    side = 1
    kudosgivere = []

    while True:
        try:
            response = requests.get(url, headers=headers, params={"per_page": per_page, "page": side})
            response.raise_for_status()
            personer = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Feil ved henting av kudos for aktivitet {aktivitet_id}: {e}")
            break

        if not personer:
            break

        kudosgivere.extend(personer)
        side += 1

    return kudosgivere
