# STRAVA-ANALYSE/python/geo.py

# Bibliotek

import contextily as ctx
import geopandas as gpd
import io
import matplotlib.pyplot as plt
import numpy as np
import polyline

from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, Normalize
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
        io.BytesIO: Et buffer bilde-objekt som kan brukes videre i bildebehandling
    """
    poly = aktivitet.get("map", {}).get("summary_polyline", None)

    if not poly:
        print("Ingen polyline-data tilgjengelig for denne aktiviteten")
        return None
    
    # Steg 1: Hent koordinater
    coords = polyline.decode(poly)
    if len(coords) < 2:
        return None

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
    start_point.plot(ax=ax, color="#00CC66", markersize=180, marker="o", edgecolor="white", linewidth=1.5, zorder=4)
    end_point.plot(ax=ax, color="#CC0000", markersize=180, marker="X", edgecolor="white", linewidth=1.5, zorder=4)

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

    # Steg 9: Generer kilometermarkører langs ruta
    streams = aktivitet.get("streams", None)
    if streams and "distance" in streams and "latlng" in streams:
        distanser = np.array(streams["distance"]["data"]) # [m]
        latlng = np.array(streams["latlng"]["data"]) # [[lat, lon], ...]

        gdf_stream = gpd.GeoDataFrame(
            geometry=[Point(lon, lat) for lat, lon in latlng],
            crs="EPSG:4326"
        ).to_crs(epsg=3857)
        
        km_coords = []
        next_km = 1000

        for i, d in enumerate(distanser):
            if d >= next_km:
                km_coords.append(gdf_stream.geometry.iloc[i])
                next_km += 1000

        if km_coords:
            for i, pt in enumerate(km_coords, start=1):
                x, y = pt.x, pt.y
                color = "#FFA726" if i % 5 == 0 else "white"
                size = 300 if i % 5 == 0 else 100
                ax.scatter(
                    x, y,
                    s=size,
                    facecolor=color,
                    linewidth=0.8,
                    alpha=0.8,
                    zorder=2
                )
                if i % 5 == 0:
                    ax.text(
                        x, y, str(i),
                        fontsize=7,
                        color="black",
                        weight="bold",
                        ha="center",
                        va="center",
                        zorder=3
                    )

    # Steg 10: Lagre til midlertidig objekt
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=dpi, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    buf.seek(0)

    # Steg 11: Lag faktisk bilde
    img = Image(buf)
    aspect = img.imageHeight / float(img.imageWidth)
    img.drawWidth = bredde
    img.drawHeight = bredde * aspect

    return img

def lag_hoydeprofil(aktivitet: dict) -> Image | None:
    """
    Lager et bilde av høydeprofilen for aktiviteten (hvis 'altitude' data finnes).

    Args:
        aktivitet (dict): Dictionary med informasjonen til aktiviteten hentet fra Strava API

    Returns:
        Image: Et ReportLab Image-objekt som kan lastes inn i PDFer
    """
    # Henter dataen
    streams = aktivitet.get("streams")
    if not streams or "altitude" not in streams or "distance" not in streams:
        print("Ingen streams-data for høydeprofil.")
        return None

    høyder = np.array(streams["altitude"]["data"])
    distanse = np.array(streams["distance"]["data"]) / 1000 # [km]

    if len(høyder) < 2:
        return None
    
    # Beregner stigning
    dh = np.gradient(høyder)
    dx = np.gradient(distanse)
    stigning = np.divide(dh, dx, out=np.zeros_like(dh), where=dx != 0)

    # Klipp ekstreme verdier for å unngå outlliers (typiske spikes)
    stigning = np.clip(stigning, -0.3, 0.3) # -30% til +30%

    # Normaliser for fargeskala
    norm = Normalize(vmin=0.3, vmax=0.3)

    # 🌈 Lag en colormap fra grønn → gul → oransje → rød
    cmap = ListedColormap(["#2ECC71", "#F1C40F", "#E67E22", "#E74C3C"])

    # Lag segmenter for LineCollection
    punkt = np.array([distanse, høyder]).T.reshape(-1, 1, 2)
    segmenter = np.concatenate([punkt[:-1], punkt[1:]], axis=1)

    lc = LineCollection(segmenter, cmap=cmap, norm=norm, linewidth=1.8)
    lc.set_array(stigning)

    # 🎨 -- Matplotlib-stil
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "axes.linewidth": 0.6,
        "axes.edgecolor": "#555555",
        "axes.labelcolor": "#333333",
        "xtick.color": "#333333",
        "ytick.color": "#333333",
        "grid.alpha": 0.3,
    })

    # Opprett figuren
    fig, ax = plt.subplots(figsize=(6, 2), dpi=300)
    ax.add_collection(lc)
    ax.autoscale()
    ax.set_xlim(distanse.min(), distanse.max())
    ax.set_ylim(høyder.min() - 5, høyder.max() + 5)

    # Bakgrunn og grid
    ax.set_facecolor("#fafafa")
    ax.grid(True, linestyle="--", linewidth=0.4)

    # Fjern ramme på topp og høyre for et mer minimalistisk uttrykk
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    # Aksene
    ax.set_xlabel("Distanse (km)", labelpad=4)
    ax.set_ylabel("Høyde (m)", labelpad=4)

    # 📏 Fargeskala
    cbar = fig.colorbar(lc, ax=ax, orientation="vertical", fraction=0.035, pad=0.02)
    cbar.set_label("Stigning")
    cbar.ax.tick_params(labelsize=7)

    # 🎯 Kilometermarkører på høydeprofil
    km_markører = np.arange(1, int(distanse.max()) + 1)
    høyde_markører = [høyder[np.argmin(np.abs(distanse - km))] for km in km_markører]

    ax.scatter(
        km_markører, høyde_markører,
        color="#1f77b4", edgecolor="white", s=20, zorder=5, linewidth=0.6
    )

    # 📸 Lagre til buffer med høy oppløsning
    buffer = io.BytesIO()
    plt.tight_layout(pad=0.3)
    fig.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)

    # Returner som ReportLab-bilde
    return Image(buffer, width=400, height=150)
