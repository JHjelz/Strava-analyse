# STRAVA-ANALYSE/private.py

# Bibliotek:

import json
import os

# Klasse:

class PrivatInfo():
    """
    Klasse for håndtering av private Strava API-data.

    Denne klassen brukes til å lagre og hente nødvendige nøkler og tokens
    som kreves for å autentisere mot Strava API-et. Tokens lagres i en
    lokal JSON-fil, slik at de kan gjenbrukes mellom kall.

    Attributter:
        token_file (str): Filbane til lokal lagring av tokens.
    """
    def __init__(self):
        """
        Initialiserer klassen med standardverdier.
        Tokens lagres i `strava_tokens.json`.
        """
        self.token_file = "strava_tokens.json"
    
    def hent_privat_info(self) -> dict:
        """
        Returnerer private API-data og tokens.

        Metoden returnerer en samlet dictionary med nødvendige data for Strava API.
        'client_id', 'client_secret' og 'authorization_code' leses fra filen,
        i tillegg til 'access_token', 'refresh_token' og 'expires_at' hvis de finnes.

        Returns:
            dict: Ordbok med følgende nøkler:
                - "client_id" (str | None): Strava-klient-ID.
                - "client_secret" (str | None): Strava-klient-hemmelighet.
                - "authorization_code" (str | None): Autorisasjonskode fra Strava (engangs).
                - "access_token" (str | None): Midlertidig tilgangstoken.
                - "refresh_token" (str | None): Token for å fornye tilgangstoken (langvarig).
                - "expires_at" (int): Unix-tidspunkt for når `access_token` utløper
        """
        tokens = self._last_tokens()
        return {
            "client_id": tokens.get("client_id"),
            "client_secret": tokens.get("client_secret"),
            "authorization_code": tokens.get("authorization_code"),
            "access_token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token"),
            "expires_at": tokens.get("expires_at", 0)
        }

    def _last_tokens(self) -> dict:
        """
        Leser inn tokens fra lokal JSON-fil.

        Hvis filen finnes, lastes alle tilgjengelige nøkler fra `self.token_file`.
        Hvis den ikke finnes, returneres en tom dictionary.

        Returns:
            dict: Dictionary med tilgjengelige Strava-data (kan være tom).
        """
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as f:
                return json.load(f)
        return {}
    
    def lagre_tokens(self, oppdatert_data: dict) -> None:
        """
        Oppdaterer og lagrer tokens i lokal JSON-fil.

        Eksisterende nøkler beholdes med mindre de er oppgitt i 'oppdatert_data',
        i så fall blir de overskrevet. Alle nøkler i den originale JSON-strukturen
        ivaretas.

        Args:
            oppdatert_data (dict): dictionary med felt som skal oppdateres.
            Eksempel:
                {
                    "access_token": "...",
                    "refresh_token": "...",
                    "expires_at": "..."
                }
        """
        with open(self.token_file, "r") as f:
            data = json.load(f)
        
        for key in data:
            if key in oppdatert_data:
                data[key] = oppdatert_data[key]
        
        with open(self.token_file, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )
