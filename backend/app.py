# backend/app.py

from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Erstatt med din Strava API access token
STRAVA_ACCESS_TOKEN = 'din_strava_access_token'
STRAVA_API_URL = "https://www.strava.com/api/v3/athlete/activities"

@app.route('/get_strava_data')
def get_strava_data():
    headers = {
        'Authorization': f'Bearer {STRAVA_ACCESS_TOKEN}'
    }
    response = requests.get(STRAVA_API_URL, headers=headers)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Kunne ikke hente data fra Strava"}), 500

if __name__ == '__main__':
    app.run(debug=True)
