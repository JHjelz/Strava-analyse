# STRAVA-ANALYSE/main.py

# Bibliotek:

from python.strava import StravaKlient

# Program:

klient = StravaKlient()

"""
Hva som finnes nå:

-[] Hent de siste 20 (x) aktivitetene dine
-[] Hent aktivitet(er) på navn
-[] Hent aktivitet(er) på dato
-[] Hent kudos-giver(e) for aktivitet på navn
-[] Hent aktivitet(er) på aktivitetstype
-[] Hente diverse rekorder
-[] Generere PDF av enkeltaktivitet
-[] Printer aktivitetene fint
-[] Printe rekorder pent og ryddig
"""

from python.aktiviteter import hent_aktiviteter, finn_aktivitet_med_navn_og_dato, hent_detaljert_aktivitet, hent_streams
from python.pdf_generator import lag_aktivitetsrapport

aktiviteter = hent_aktiviteter(klient.access_token) # finn_aktivitet_med_navn_og_dato(klient.access_token, "NC", "21-09-2025")
aktivitet = aktiviteter[0]
aktivitet = hent_detaljert_aktivitet(klient.access_token, aktivitet["id"])
streams = hent_streams(klient.access_token, aktivitet["id"])

if streams:
    aktivitet["streams"] = streams
    lag_aktivitetsrapport(aktivitet)
