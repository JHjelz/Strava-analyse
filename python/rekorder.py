# STRAVA-ANALYSE/python/rekorder.py

# Bibliotek

import heapq
import requests
from tqdm import tqdm

# Funksjoner

def finn_rekorder(access_token: str, per_page: int=200) -> dict:
    """
    Henter alle aktiviteter fra Strava og finner ulike 'rekorder' / 'ekstremalverdier',
    både samlet og delt opp etter aktivitetstype (Run, Ride, Swim, ...).

    Args:
        access_token (str): Gyldig Strava access token
        per_page (int, optional): Antall aktiviteter per API-kall (maks 200)

    Returns:
        dict: Dictionary med ekstremalverdier og aktivitetene som matcher
    """
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    globale_kategorier = {
        "flest_kudos": ("kudos_count", 10),
        "flest_kommentarer": ("comment_count", 3)
    }

    per_type_kategorier = {
        "lengste": ("distance", 3),
        "varighet": ("moving_time", 3),
        "flest_høydemeter": ("total_elevation_gain", 3),
        "brattest": {"_bratthet", 3},
        "raskeste_snittfart": ("average_speed", 3),
        "maksfart": ("max_speed", 3)
    }

    heaps_global = {k: [] for k in globale_kategorier}
    heaps_per_type = {}

    side = 1
    while True:
        respons = requests.get(url, headers=headers, params={"per_page": per_page, "page": side})
        respons.raise_for_status()
        aktiviteter = respons.json()

        if not aktiviteter:
            break

        for akt in tqdm(aktiviteter, desc=f"Sjekker side {side}", colour="yellow", leave=False):
            akt_id = akt.get("id")
            akt_type = akt.get("type", "Unknown")

            # --- Globale kategorier ---
            for kategori, (felt, n) in globale_kategorier.items():
                verdi = akt.get(felt, 0)
                if len(heaps_global[kategori]) < n:
                    heapq.heappush(heaps_global[kategori], (verdi, akt_id, akt))
                else:
                    heapq.heappushpop(heaps_global[kategori], (verdi, akt_id, akt))
            
            # --- Per-type kategorier ---
            for kategori, (felt, n) in per_type_kategorier.items():
                if felt == "_bratthet":
                    dist = akt.get("distance", 0)
                    gain = akt.get("total_elevation_gain", 0)
                    verdi = (gain / dist) if dist > 0 else 0
                else:
                    verdi = akt.get(felt, 0)
                key = (kategori, akt_type)
                if key not in heaps_per_type:
                    heaps_per_type[key] = []
                if len(heaps_per_type[key]) < n:
                    heapq.heappush(heaps_per_type[key], (verdi, akt_id, akt))
                else:
                    heapq.heappushpop(heaps_per_type[key], (verdi, akt_id, akt))

        side += 1
    
    resultater = {
        kategori: [akt for _, _, akt in sorted(heap, key=lambda x: x[0], reverse=True)]
        for kategori, heap in heaps_global.items()
    }

    resultater_per_type = {
        f"{kategori}_{akt_type}": [
            akt for _, _, akt in sorted(heap, key=lambda x: x[0], reverse=True)
        ]
        for (kategori, akt_type), heap in heaps_per_type.items()
    }

    resultater.update(resultater_per_type)
    
    return resultater
