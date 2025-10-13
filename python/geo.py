# STRAVA-ANALYSE/python/geo.py

# Bibliotek

import polyline
import matplotlib.pyplot as plt

# Funksjoner

def lag_rutekart(aktivitet: dict, filnavn: str="rute.png") -> None:
    """
    Tegner ruten til aktiviteten basert på summary_polyline og lagrer som png-fil.

    Args:
        aktivitet (dict): Dictionary med informasjonen til aktiviteten hentet fra Strava API
        filnavn (str): Streng med filstien til png-filen som skal genereres (default: "rute.png")
    """
    poly = aktivitet.get("map", {}).get("summary_polyline", None)

    if not poly:
        print("Ingen polyline-data tilgjengelig for denne aktiviteten")
        return None
    
    coords = polyline.decode(poly)
    lats, lons = zip(*coords)

    plt.figure(figsize=(6, 6))
    plt.plot(lons, lats, color="red", linewidth=2)
    plt.scatter(lons[0], lats[0], color="green", label="Start")
    plt.scatter(lons[-1], lats[-1], color="blue", label="Slutt")
    plt.legend()
    plt.axis("off")
    plt.savefig(filnavn, dpi=300, bbox_inches="tight")
    plt.close()

    return filnavn
