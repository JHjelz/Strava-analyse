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
-[] Printer aktivitetene fint
-[] Printe rekorder pent og ryddig
"""

from python.aktiviteter import hent_aktiviteter
from python.geo import lag_rutekart
from python.pdf_generator import lag_aktivitetsrapport

aktiviteter = hent_aktiviteter(klient.access_token)

aktivitet = aktiviteter[0]

lag_rutekart(aktivitet)

lag_aktivitetsrapport(aktivitet)
