# STRAVA-ANALYSE/python/geo.py

# Bibliotek

import contextily as ctx
import geopandas as gpd
import io
import matplotlib.pyplot as plt
import polyline

from reportlab.platypus import Image
from shapely.geometry import LineString, Point

# Funksjoner

def lag_rutekart(aktivitet: dict, bredde: float) -> io.BytesIO:
    """
    Tegner ruten til aktiviteten oppå et kart og returnerer som et io-objekt.
    Bruker OpenStreetMap-fliser via contextily.

    Args:
        aktivitet (dict): Dictionary med informasjonen til aktiviteten hentet fra Strava API
        bredde (float): Bredden på kartet som skal genereres

    Returns:
        Image: ReportLab Image-objekt klart til å puttes rett inn i PDF
    """
    poly = aktivitet.get("map", {}).get("summary_polyline", None)

    if not poly:
        print("Ingen polyline-data tilgjengelig for denne aktiviteten")
        return None
    
    # Steg 1: Hent koordinater
    coords = polyline.decode(poly)

    # Steg 2: Lag GeoDataFrame med ruten
    linje = LineString([(lon, lat) for lat, lon in coords])
    gdf = gpd.GeoDataFrame(geometry=[linje], crs="EPSG:4326").to_crs(epsg=3857)

    # Steg 3: Hent justert bounding box
    padding_factor = 0.2
    minx, miny, maxx, maxy = gdf.total_bounds
    dx = (maxx - minx) * padding_factor
    dy = (maxy - miny) * padding_factor
    minx, maxx = minx - dx, maxx + dx
    miny, maxy = miny - dy, maxy + dy

    # Steg 4: Sett størrelsen på figuren
    bredde_px = 1500
    dpi = 150
    bredde_inn = bredde_px / dpi
    hoyde_inn = bredde_inn * 0.7

    # Steg 5: Plot
    fig, ax = plt.subplots(figsize=(bredde_inn, hoyde_inn))
    gdf.plot(ax=ax, color="#FF6F00", linewidth=3)

    # Steg 6: Marker start- og sluttpunkt
    start_lon, start_lat = coords[0][1], coords[0][0]
    end_lon, end_lat = coords[-1][1], coords[-1][0]
    start_point = gpd.GeoSeries([Point(start_lon, start_lat)], crs="EPSG:4326").to_crs(epsg=3857)
    end_point = gpd.GeoSeries([Point(end_lon, end_lat)], crs="EPSG:4326").to_crs(epsg=3857)
    start_point.plot(ax=ax, color="#00CC66", markersize=180, marker="o", edgecolor="white", linewidth=1.5, zorder=3)
    end_point.plot(ax=ax, color="#CC0000", markersize=180, marker="X", edgecolor="white", linewidth=1.5, zorder=3)

    # Steg 7: Tilpass aspect til figuren
    fig_aspect = bredde_inn / hoyde_inn
    bbox_bredde = maxx - minx
    bbox_hoyde = maxy - miny
    bbox_aspect = bbox_bredde / bbox_hoyde

    if bbox_aspect > fig_aspect:
        ny_hoyde = bbox_bredde / fig_aspect
        ekstra = (ny_hoyde - bbox_hoyde) / 2
        miny -= ekstra
        maxy += ekstra
    else:
        ny_bredde = bbox_hoyde * fig_aspect
        ekstra = (ny_bredde - bbox_bredde) / 2
        minx -= ekstra
        maxx += ekstra
    
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_axis_off()

    # Steg 8: Legg til bakgrunnskart
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

    # Steg 9: Lagre til midlertidig objekt
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=dpi, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    buf.seek(0)

    # Steg 10: Lag faktisk bilde
    img = Image(buf)
    aspect = img.imageHeight / float(img.imageWidth)
    img.drawWidth = bredde
    img.drawHeight = bredde * aspect

    return img
