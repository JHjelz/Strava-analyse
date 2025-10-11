# STRAVA-ANALYSE/main.py

# Bibliotek:

from python.strava import StravaKlient

# Program:

klient = StravaKlient()

from python.aktiviteter import hent_aktiviteter, finn_aktiviteter_med_type, finn_aktiviteter_paa_dato
from python.visning import fin_print

aktiviteter = finn_aktiviteter_med_type(klient.access_token, "Terrengløp")
fin_print(aktiviteter)

"""
Hva som finnes nå:

-[] Hent de siste 20 (x) aktivitetene dine
-[] Hent aktivitet(er) på navn
-[] Hent aktivitet(er) på dato
-[] Hent kudos-giver(e) for aktivitet på navn
-[] Hent aktivitet(er) på aktivitetstype
-[] Printer aktivitetene fint
"""
