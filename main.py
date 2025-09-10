from privat import privat_info
from python.tilgang import sikre_tokens

#
import requests
#

info = privat_info()

access_token, refresh_token = sikre_tokens(info)

#
def get_activities(access_token, per_page=5):
    """Henter aktiviteter fra Strava."""
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, params={"per_page": per_page})
    response.raise_for_status()
    return response.json()

activities = get_activities(access_token)

print("\nDine siste aktiviteter:\n")
for act in activities:
    print(f"{act['name']} - {act['distance']/1000:.2f} km - {act['start_date_local']}")
#
