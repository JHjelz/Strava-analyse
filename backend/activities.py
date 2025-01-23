# backend/activities.py

import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_all_activities(access_token, activities_per_page=100):
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
        page += 1
    
    if len(all_activities) == 0:
        return None
    return all_activities