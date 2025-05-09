# app.py

from flask import Flask, render_template
from flask_cors import CORS

from backend.access import access_bp, socketio
from backend.activities import activities_bp

app = Flask(__name__)
CORS(app, origins=["https://jhjelz.github.io"])

# Initialiser SocketIO med Flask-appen
socketio.init_app(app)

# Registrer Blueprints:
app.register_blueprint(access_bp, url_prefix="/access")
app.register_blueprint(activities_bp, url_prefix="/activities")

@app.route('/')
def index():
    return render_template('index.html') # Viser HTML-siden

if __name__ == '__main__':
    app.run(debug=True)
