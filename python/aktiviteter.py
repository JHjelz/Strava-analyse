# STRAVA-ANALYSE/python/aktiviteter.py

# Bibliotek

import requests
from datetime import datetime

# Funksjoner

def hent_aktiviteter(access_token: str, per_page: int = 20) -> list[dict]:
    """
    Henter aktiviteter fra Strava API for den autentiserte brukeren.

    Denne funksjonen kaller Stravas endpoint `/athlete/activities` og returnerer
    en liste med aktivitetsdata (løp, sykling, svømming osv.).
    Antall aktiviteter kan begrenses med `per_page`.

    Args:
        access_token (str): Gyldig Strava access token for brukeren.
        per_page (int, optional): Antall aktiviteter som skal hentes per kall.
            Standard er 20. Strava tillater opptil 200.

    Returns:
        list[dict]:
            En liste med aktiviteter i JSON-format (dict-objekter).
            Hver aktivitet inneholder nøkkelinformasjon som:
            - id (int): Strava-ID for aktiviteten.
            - name (str): Navn på aktiviteten (ofte gitt av bruker eller Strava).
            - distance (float): Distanse i meter.
            - moving_time (int): Bevegelsestid i sekunder.
            - type (str): Aktivitetstype (f.eks. "Run", "Ride", "Swim").
            - start_date (str): Starttidspunkt i ISO 8601-format.
            ... og flere felt avhengig av Strava API.
        Returnerer [] hvis noe feiler.
    """
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        respons = requests.get(url, headers=headers, params={"per_page": per_page})
        respons.raise_for_status()
        return respons.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP-feil ved henting av aktiviteter: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Feil ved forespørsel til Strava API: {e}")
    except ValueError as e:
        print(f"Feil ved parsing av respons: {e}")
    return []

def finn_aktiviteter_med_navn(access_token: str, navn: str, maks_treff: int = 20, per_page: int = 200) -> list[dict]:
    """
    Søker gjennom alle brukerens aktiviteter og returnerer de som matcher navnet.

    Args:
        access_token (str): Gyldig Strava access token for brukeren.
        navn (str): Tekststreng som skal matches mot aktivitetens navn.
                    Treffer både eksakt og delvis samsvar (case-insensitive).
        maks_treff (int, optional): Maks antall aktiviteter som returneres. Default er 20.
        per_page (int, optional): Antall aktiviteter å hente per API-kall. Default er 200 (maks).

    Returns:
        list[dict]: Liste med aktiviteter (dict) som matcher søket.
    """
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    navn =  navn.lower()
    
    side = 1
    treff = []

    while len(treff) < maks_treff:
        try:
            respons = requests.get(url, headers=headers, params={"per_page": per_page, "page": side})
            respons.raise_for_status()
            aktiviteter = respons.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Feil ved henting av aktiviteter: {e}")
            break

        # Hvis vi har nådd slutten (ingen flere aktiviteter fra API)
        if not aktiviteter:
            break

        # Filtrer på navn (case-insensitive søk)
        for aktivitet in aktiviteter:
            if navn in aktivitet["name"].lower():
                treff.append(aktivitet)
                if len(treff) >= maks_treff:
                    break

        side += 1  # Neste side

    return treff

def finn_aktiviteter_paa_dato(access_token: str, dato_str: str, per_page: int = 200) -> list[dict]:
    """
    Henter alle aktiviteter som ble utført på en spesifikk dato.

    Stopper automatisk når vi har gått forbi datoen.

    Args:
        access_token (str): Gyldig Strava access token for brukeren.
        dato_str (str): Dato på formatet "dd-mm-åååå", f.eks. "04-09-2025".
        per_page (int, optional): Antall aktiviteter å hente per API-kall. Default er 200 (maks).

    Returns:
        list[dict]: Liste med aktiviteter (dict) som fant sted på valgt dato.
    """
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}

    valgt_dato = datetime.strptime(dato_str, "%d-%m-%Y").date()
    side = 1
    treff = []

    while True:
        try:
            respons = requests.get(url, headers=headers, params={"per_page": per_page, "page": side})
            respons.raise_for_status()
            aktiviteter = respons.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Feil ved henting av aktiviteter: {e}")
            break

        if not aktiviteter:  # Ingen flere aktiviteter
            break

        for aktivitet in aktiviteter:
            akt_dato = datetime.fromisoformat(aktivitet["start_date_local"].split("Z")[0]).date()

            if akt_dato < valgt_dato:
                # Alle resterende aktiviteter vil være eldre, vi kan stoppe
                return treff

            if akt_dato == valgt_dato:
                treff.append(aktivitet)

        side += 1

    return treff

def finn_aktiviteter_med_type(access_token: str, aktivitetstype: str, maks_treff: int = 20, per_page: int = 200) -> list[dict]:
    """
    Søker gjennom brukerens aktiviteter og returnerer de siste aktivitetene av valgt type.

    Args:
        access_token (str): Gyldig Strava access token for brukeren.
        aktivitetstype (str): Type aktivitet (norsk, f.eks. 'løp', 'sykkel', 'svømming').
                              Mappes internt til Strava sine typer ('Run', 'Ride', 'Swim', ...).
        maks_treff (int, optional): Antall aktiviteter som returneres. Default = 20.
        per_page (int, optional): Antall aktiviteter som hentes per API-kall. Default = 200 (maks).

    Returns:
        list[dict]: Liste med aktiviteter (dict) som matcher søket.
    """
    # Norsk -> Strava mapping
    type_map = {
        "løp": ("type", "Run"),
        "sykkel": ("type", "Ride"),
        "svømming": ("type", "Swim"),
        "gåtur": ("type", "Walk"),
        "fjelltur": ("type", "Hike"),
        "terrengløp": ("sport_type", "TrailRun")
    }

    aktivitetstype = aktivitetstype.lower()
    if aktivitetstype not in type_map:
        print(f"Ukjent aktivitetstype: {aktivitetstype}. Gyldige er: {', '.join(type_map.keys())}")
        return []

    strava_felt, strava_aktivitet = type_map[aktivitetstype]

    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}

    side = 1
    treff = []

    while len(treff) < maks_treff:
        try:
            respons = requests.get(url, headers=headers, params={"per_page": per_page, "page": side})
            respons.raise_for_status()
            aktiviteter = respons.json()
        except requests.exceptions.RequestException as e:
            print(f"Feil ved henting av aktiviteter: {e}")
            break

        if not aktiviteter:
            break  # ingen flere aktiviteter fra API

        # Filtrer på valgt type
        for aktivitet in aktiviteter:
            if aktivitet.get(strava_felt, "N/A") == strava_aktivitet:
                treff.append(aktivitet)
                if len(treff) >= maks_treff:
                    break

        side += 1

    return treff
