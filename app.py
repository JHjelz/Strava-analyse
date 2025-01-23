# backend/app.py

from flask import Flask, render_template, jsonify, request
import logging

from backend.access import refresh_access_token, get_access_token
from backend.activities import get_all_activities
from backend.private import CLIENT_ID, CLIENT_SECRET, AUTHORIZATION_CODE

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html') # Viser HTML-siden

@app.route('/get_strava_data', methods=['POST'])
def get_strava_data():
    data = request.get_json()
    client_id = data.get('client_id')
    client_secret = data.get('client_secret')
    refresh_token = data.get('refresh_token')

    if not client_id or not client_secret or not refresh_token:
        return jsonify({"error": "Manglende nødvendige parametre"}), 400

    # Hent eller oppdater tokens
    access_token, refresh = refresh_access_token(client_id, client_secret, refresh_token)
    
    if not access_token:
        return jsonify({"error": "Kunne ikke hente access token"}), 400

    activities = get_all_activities(access_token)

    if activities:
        return jsonify(activities)
    else:
        return jsonify({"error": "Kunne ikke hente data fra Strava"}), 500

if __name__ == '__main__':
    app.run(debug=True)
