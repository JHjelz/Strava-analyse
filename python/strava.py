# STRAVA-ANALYSE/python/strava.py

# Bibliotek:

from privat import PrivatInfo
from python.tilgang import sikre_tokens

# Klasse:

class StravaKlient:
    """
    Strava-klient som håndterer autentisering og tokens mot Strava API-et.

    Klassen fungerer som inngangspunkt til systemet. Ved opprettelse
    sørger den for at gyldige tokens er tilgjengelige, ved å bruke
    `PrivatInfo` og `sikre_tokens`.

    Attributter:
        info (PrivatInfo): Holder konfigurasjon og lagrede Strava-tokens.
        access_token (str | None): Gyldig access token som kan brukes mot API-et (None ved feil).
        refresh_token (str | None): Refresh token knyttet til access_token (None ved feil).
    """

    def __init__(self):
        """
        Initialiserer Strava-klienten.

        Oppretter et `PrivatInfo`-objekt og sørger for at gyldige tokens
        er tilgjengelige ved oppstart. Tokens hentes enten fra lokal lagring
        eller oppdateres via Strava API-et.
        """
        self.info = PrivatInfo()
        self.access_token, self.refresh_token = sikre_tokens(self.info)
