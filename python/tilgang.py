# STRAVA-ANALYSE/python/tilgang.py

# Bibliotek:

import requests
import time

from privat import PrivatInfo

# Funksjoner:

def oppdater_access_token(client_id: str, client_secret: str, refresh_token: str) -> tuple[str | None, str | None, str | None]:
    """
    Henter nytt access_token og refresh_token fra Strava API.

    Brukes når access_token har utløpt. Funksjonen kalles som regel
    automatisk fra 'sikre_tokens', men kan også brukes manuelt.

    Args:
        client_id (str): Strava-klient-ID.
        client_secret (str): Strava-klient-hemmelighet.
        refresh_token (str): Gammelt refresh token som brukes for å hente nye tokens.

    Returns:
        tuple[str | None, str | None, int | None]:
            - access_token (str | None): Nytt access token.
            - refresh_token (str | None): Nytt refresh token.
            - expires_at (int | None): Unix timestamp for når access token utløper.
            Hvis noe går galt returneres (None, None, None).
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
        return (
            response_data["access_token"],
            response_data["refresh_token"],
            response_data["expires_at"],
        )
    except requests.exceptions.RequestException as e:
        print(f"Feil under oppdatering av access_token: {e}")
        return None, None, None

def hent_access_token(client_id: str, client_secret: str, authorization_code: str) -> tuple[str | None, str | None, str | None]:
    """
    Henter nytt access_token og refresh_token ved bruk av authorization_code.

    Dette er **første steg i oppsettet** av Strava-tilgang.
    Authorization_code hentes manuelt fra Strava ved å følge instruksjonene:

        1. Åpne lenken i nettleseren med din `client_id`:
           https://www.strava.com/oauth/authorize?client_id=ID&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=read_all,activity:read_all
        2. Trykk "Authorize" på Strava-siden.
        3. Du blir sendt til en lokal side, f.eks.:
           http://localhost/?state=&code=AUTHORIZATION_CODE&scope=read,activity:read_all,read_all
        4. Kopier verdien `AUTHORIZATION_CODE` fra lenken.
        5. Kall denne funksjonen med koden.

    Args:
        client_id (str): Strava-klient-ID.
        client_secret (str): Strava-klient-hemmelighet.
        authorization_code (str): Engangskode hentet manuelt fra Strava.

    Returns:
        tuple[str | None, str | None, int | None]:
            - access_token (str | None): Nytt access token.
            - refresh_token (str | None): Nytt refresh token.
            - expires_at (int | None): Unix timestamp for når access token utløper.
            Hvis noe går galt returneres (None, None, None).
    """
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
        return (
            response_data["access_token"],
            response_data["refresh_token"],
            response_data["expires_at"],
        )
    except requests.exceptions.RequestException as e:
        print(f"Feil under oppdatering av access_token: {e}")
        return None, None, None

def sikre_tokens(info: PrivatInfo) -> tuple[str | None, str | None]:
    """
    Sørger for atgyldige tokens er tilgjengelige og oppdaterer dem ved behov.

    Logikken er:
        - Hvis ingen tokens er lagret: henter nye med authorization_code.
        - Hvis access_token er utløpt: oppdaterer med refresh_token.
        - Hvis access_token fortsatt er gyldig: returnerer eksisterende tokens.

    Bruk denne funksjonen som hovedinngang for å hente gyldige tokens til API-kall.

    Args:
        info (PrivatInfo): Et PrivatInfo-objekt som holder client_id,
            client_secret, authorization_code og eventuelle tokens.

    Returns:
        tuple[str | None, str | None]:
            - access_token (str | None): Gyldig access token.
            - refresh_token (str | None): Refresh token knyttet til access token.
    """
    kreditering = info.hent_privat_info()
    client_id = kreditering.get("client_id")
    client_secret = kreditering.get("client_secret")
    access_token = kreditering.get("access_token")
    refresh_token = kreditering.get("refresh_token")
    expires_at = kreditering.get("expires_at", 0)

    now = int(time.time())

    if not access_token or not refresh_token:
        print("Ingen tokens funnet, henter nye med authorization_code...")
        access_token, refresh_token, expires_at = hent_access_token(
            client_id, client_secret, kreditering["authorization_code"]
        )
        if access_token:
            info.lagre_tokens({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_at": expires_at
            })
    elif now >= expires_at:
        print("Access_token er utløpt, oppdaterer tokens med refresh_token...")
        new_access_token, new_refresh_token, new_expires_at = oppdater_access_token(
            client_id, client_secret, refresh_token
        )
        if new_access_token:
            access_token, refresh_token, expires_at = new_access_token, new_refresh_token, new_expires_at
            info.lagre_tokens({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_at": expires_at,
            })
    else:
        print(f"Access token er fortsatt gyldig i {expires_at - now} sekunder.")
    return access_token, refresh_token
