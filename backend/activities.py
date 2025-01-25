# backend/activities.py

# Bibliotek:

from flask import Blueprint
import logging
import requests

# Variabler:

activities_bp = Blueprint('activities', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Funksjoner:

def get_all_activities(access_token, socketio, activities_per_page=100):
    """Henter alle tilgjengelige aktiviteter ved å iterere over alle sider med resultater.

    Args:
        access_token (str): Strava tilgangstoken.
        activities_per_page (int): Antall aktiviteter per side (default er 100, Stravas maksgrense).

    Returns:
        list: En liste med alle aktiviteter som er hentet.
    """
    headers = {'Authorization': f'Bearer {access_token}'}
    all_activities = []
    page = 1

    response = requests.get('https://www.strava.com/api/v3/athlete', headers=headers)
    if response.status_code != 200:
        logger.error("Feil ved henting av atlet-data: %d", response.status_code)
    athlete_id = response.json()["id"]
    response = requests.get(f'https://www.strava.com/api/v3/athletes/{athlete_id}/stats', headers=headers)
    if response.status_code != 200:
        logger.error("Feil ved henting av statistikk: %d", response.status_code)
        return None
    stats = response.json()
    keys = []
    total_activities = 0
    for key in stats:
        if 'all' in key:
            keys.append(key)
    print(keys)
    for el in keys:
        total_activities += int(stats[el]["count"])
    if total_activities == 0:
        return all_activities
    total_pages = (total_activities // activities_per_page) + (1 if total_activities % activities_per_page else 0)

    while True:
        response = requests.get(
            'https://www.strava.com/api/v3/athlete/activities',
            headers=headers,
            params={'page': page, 'per_page': activities_per_page}
        )
        
        if response.status_code != 200:
            logger.error("Feil ved henting av data på side %s: %d", page, response.status_code)
            break
        
        activities = response.json()
        if not activities:
            break
        
        all_activities.extend(activities)

        progress = min(int((page / total_pages) * 100), 100)
        socketio.emit('progress', {'progress': progress})

        page += 1
    
    socketio.emit('progress', {'progress': 100})

    return all_activities if all_activities else None

# Routes:
