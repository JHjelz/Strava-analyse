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

from python.rekorder import finn_rekorder
from python.visning import fin_print_av_rekorder

rekorder = finn_rekorder(klient.access_token)

fin_print_av_rekorder(rekorder)
