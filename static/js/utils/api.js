// frontend/js/utils/api.js

// Hente data fra Strava:
async function get_strava_data() {
    const id = document.getElementById("idInput");
    const secret = document.getElementById("secretInput");
    const refresh = document.getElementById("refreshInput");
    const box = document.getElementById("data-field");

    let bool = false;

    // Validering:
    [id, secret, refresh].forEach(input => {
        if (input.value === "") {
            input.classList.add("warning");
            input.value = "Ugyldig verdi!";
            bool = true;
        }
    })

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
                refresh_token: refresh.value,
            }),
          });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Ukjent feil");
        }
    
        const data = await response.json();
        sessionStorage.setItem("StravaData", JSON.stringify(data)); // Lagre data i StravaData
        box.innerHTML = `
        <h2>Strava-data lastet ned</h2>
        <br>
        <p>Begynn å analysere data!</p>`;
        [id, secret, refresh].forEach(input => {
            input.value = "";
        })
        toggleLeftSidebar();
        document.getElementById('right-sidebar-btn').style.display = 'block';
    } catch (error) {
        box.innerHTML = `
        <h2>Feil</h2>
        <br>
        <p>Det oppsto en feil under nedlasting av Strava-data!</p>
        <p>Detaljer: ${error.message}</p>`;
    }
}