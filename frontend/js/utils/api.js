// frontend/js/utils/api.js

const StravaData = [];

// Hente data fra Strava:
async function get_strava_data() {
    const id = document.getElementById("idInput");
    const secret = document.getElementById("secretInput");
    const authorization = document.getElementById("authorizationInput");

    let bool = false;

    if (id.value === "") {
        id.value = "Ugyldig verdi!";
        id.classList.add("warning");
        bool = true;
    }
    if (secret.value === "") {
        secret.value = "Ugyldig verdi!";
        secret.classList.add("warning");
        bool = true;
    }
    if (authorization.value === "") {
        authorization.value = "Ugyldig verdi!";
        authorization.classList.add("warning");
        bool = true;
    }

    if (bool) {
        return;
    }

    try {
        const response = await fetch('/get_strava_data', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                client_id: id.value,
                client_secret: secret.value,
                authorization_code: authorization.value,
            }),
          });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Ukjent feil");
        }
    
        const data = await response.json();
        StravaData.push(...data); // Lagre data i StravaData
        const box = document.getElementById("data-field");
        box.innerHTML = `
            <h2>Strava-data lastet ned</h2>
            <br>
            <p>Data: ${JSON.stringify(data)}</p>`;
        
    } catch (error) {
        const box = document.getElementById("data-field");
        box.innerHTML = "";
        box.innerHTML = "<h2>Feil</h2><br><p>...under nedlasting av Strava-data!</p>"
    }

    /*const box = document.getElementById("data-field");
    box.innerHTML = "";
    box.innerHTML = "<h2>Strava-data lastet ned</h2><br><p>Begynn å analyser data!</p>";*/
}
