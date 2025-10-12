# STRAVA-ANALYSE/python/visning.py

# Bibliotek

from datetime import datetime

# Funksjoner

def sekunder_til_tid(sek: int) -> str:
    """
    Konverterer sekunder til H:MM:SS.
    
    Args:
        sek (int): Tid i sekunder
    
    Returns:
        str: Streng med tid vist som (timer:)minutter:sekunder
    """
    timer = sek // 3600
    minutter = (sek % 3600) // 60
    sekunder = sek % 60
    if timer > 0:
        return f"{timer}:{minutter:02}:{sekunder:02}"
    else:
        return f"{minutter}:{sekunder:02}"

def beregn_pace_eller_hastighet(distance_m: float, moving_time_s: int, aktivitetstype: str) -> str:
    """
    Returnerer enten pace (min/km) eller hastighet (km/t).

    Args:
        distance_m (float): Aktivitetens distanse i meter
        moving_time_s (int): Aktivitetens varighet i sekunder
        aktivitetstype (str): Løp/sykkel/...
    
    Returns:
        str: Aktivitetens pace hvis løping som min:sek/km, ellers hastighet som km/h
    """
    distance_km = distance_m / 1000
    if distance_km == 0 or moving_time_s == 0:
        return "-"
    
    if aktivitetstype.lower() == "run":
        pace = moving_time_s / 60 / distance_km  # min/km
        minutter = int(pace)
        sekunder = int((pace - minutter) * 60)
        return f"{minutter}:{sekunder:02}/km"
    else:
        hastighet = distance_km / (moving_time_s / 3600)  # km/t
        return f"{hastighet:.1f} km/t"

def fin_print(aktiviteter: list[dict]) -> None:
    """
    Printer en pen oversikt over aktiviteter:
    Dato - navn - type - klokkeslett - tid - distanse - tempo/hastighet - kudos - kommentarer

    Args:
        aktiviteter (list[dict]): En liste av aktiviter på dictionary-format
    """
    for akt in aktiviteter:
        dato = datetime.fromisoformat(akt["start_date"].replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
        navn = akt.get("name", "Uten navn")
        akt_type = akt.get("type", "?")
        akt_variant = akt.get("sport_type", "?")
        tid = sekunder_til_tid(akt.get("moving_time", 0))
        distanse_km = akt.get("distance", 0) / 1000
        fart = beregn_pace_eller_hastighet(akt.get("distance", 0), akt.get("moving_time", 0), akt_type)
        kudos = akt.get("kudos_count", 0)
        kommentarer = akt.get("comment_count", 0)

        if akt_type != akt_variant:
            streng = f"{dato} - {navn} - {akt_type} ({akt_variant}) - Tid: {tid} - Distanse: {distanse_km:.2f} km - {fart} - Kudos: {kudos} - Kommentarer: {kommentarer}"
        else:
            streng = f"{dato} - {navn} - {akt_type} - Tid: {tid} - Distanse: {distanse_km:.2f} km - {fart} - Kudos: {kudos} - Kommentarer: {kommentarer}"
        
        print(streng)

def fin_print_av_rekorder(rekorder: dict) -> None:
    """
    Printer rekordene i et ryddig oppsett.

    Args:
        rekorder (dict): Dictionary fra finn_rekorder()
    """
    globale_kategorier = ["flest_kudos", "flest_kommentarer"]

    print("\n=== GLOBALE REKORDER ===")
    for kategori, aktiviteter in rekorder.items():
        if kategori in globale_kategorier:
            print(f"\n--- {kategori.replace('_', ' ').title()} ---")
            for akt in aktiviteter:
                dato = datetime.fromisoformat(akt["start_date"].replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
                navn = akt.get("name", "Uten navn")
                akt_type = akt.get("type", "?")
                tid = sekunder_til_tid(akt.get("moving_time", 0))
                distanse_km = akt.get("distance", 0) / 1000
                fart = beregn_pace_eller_hastighet(akt.get("distance", 0), akt.get("moving_time", 0), akt_type)
                kudos = akt.get("kudos_count", 0)
                kommentarer = akt.get("comment_count", 0)
                print(f"{dato} - {navn} - {akt_type} - Tid: {tid} - Distanse: {distanse_km:.2f} km - {fart} - Kudos: {kudos} - Kommentarer: {kommentarer}")

    print("\n=== REKORDER PER AKTIVITETSTYPE ===")
    per_type_kategorier = {}
    for nøkkel in rekorder:
        if nøkkel in globale_kategorier:
            continue
        if "_" in nøkkel:
            kategori, akt_type = nøkkel.rsplit("_", 1)
            if kategori not in per_type_kategorier:
                per_type_kategorier[kategori] = {}
            per_type_kategorier[kategori][akt_type] = rekorder[nøkkel]

    for kategori, typer in per_type_kategorier.items():
        print(f"\n--- {kategori.replace('_', ' ').title()} ---")
        for akt_type, aktiviteter in typer.items():
            print(f"\n** {akt_type} **")
            for akt in aktiviteter:
                dato = datetime.fromisoformat(akt["start_date"].replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
                navn = akt.get("name", "Uten navn")
                tid = sekunder_til_tid(akt.get("moving_time", 0))
                distanse_km = akt.get("distance", 0) / 1000
                fart = beregn_pace_eller_hastighet(akt.get("distance", 0), akt.get("moving_time", 0), akt_type)
                kudos = akt.get("kudos_count", 0)
                kommentarer = akt.get("comment_count", 0)
                print(f"{dato} - {navn} - Tid: {tid} - Distanse: {distanse_km:.2f} km - {fart} - Kudos: {kudos} - Kommentarer: {kommentarer}")
