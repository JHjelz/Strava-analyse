// frontend/js/startStrava.js

let stravaData = []; // For å lagre Strava-dataene

// Funksjon for å laste ned data fra Strava
function fetchStravaData() {
    fetch('/get_strava_data')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('data-field').innerText = data.error;
            } else {
                stravaData = data;
                document.getElementById('analyze-btn').style.display = 'inline-block'; // Vis "Analyser data"-knapp
                displayData(stravaData); // Vis dataene i hovedfeltet
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            document.getElementById('data-field').innerText = 'Kunne ikke hente data.';
        });
}

// Funksjon for å vise dataene i hovedfeltet
function displayData(data) {
    const dataField = document.getElementById('data-field');
    dataField.innerHTML = ''; // Tøm eksisterende innhold

    data.forEach(activity => {
        const activityDiv = document.createElement('div');
        activityDiv.innerHTML = `
            <h3>${activity.name}</h3>
            <p>Type: ${activity.type}</p>
            <p>Distance: ${(activity.distance / 1000).toFixed(2)} km</p>
            <p>Time: ${(activity.moving_time / 60).toFixed(2)} min</p>
            <p>Date: ${new Date(activity.start_date).toLocaleString()}</p>
        `;
        dataField.appendChild(activityDiv);
    });
}

// Funksjon for å analysere data
function analyzeData() {
    const totalDistance = stravaData.reduce((sum, activity) => sum + activity.distance, 0);
    const totalTime = stravaData.reduce((sum, activity) => sum + activity.moving_time, 0);
    const averagePace = totalTime / totalDistance;

    const analysisResult = `
        <h2>Analyse Resultater:</h2>
        <p>Total Distance: ${(totalDistance / 1000).toFixed(2)} km</p>
        <p>Total Time: ${(totalTime / 60).toFixed(2)} min</p>
        <p>Average Pace: ${(averagePace).toFixed(2)} min/km</p>
    `;
    document.getElementById('data-field').innerHTML = analysisResult;
}