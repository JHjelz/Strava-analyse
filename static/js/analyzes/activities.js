// static/js/analyzes/activities.js

function showActivities() {
    const activities = JSON.parse(sessionStorage.getItem("StravaData"));
    const container = document.getElementById("data-field");

    container.innerHTML = '';

    activities.forEach(activity => {
        // Lag hoveddiven for aktiviteten
        const activityDiv = createDiv();
        activityDiv.classList.remove("flex-container");
        activityDiv.classList.add("activity");

        // Lag en div for info (Type, Dato, Varighet, Avstand)
        const info = createDiv();
        info.innerHTML = `
            <p><strong>Type:</strong> ${activity.type}</p>
            <p><strong>Dato:</strong> ${new Date(activity.start_date).toLocaleDateString()}</p>
            <p><strong>Varighet:</strong> ${formatDuration(activity.elapsed_time)}</p>
            <p><strong>Avstand:</strong> ${(activity.distance / 1000).toFixed(3)} km</p>
        `;

        // Sett aktivitetens navn i activityDiv
        const activityHeader = document.createElement("h3");
        activityHeader.textContent = activity.name;

        // Legg til activityHeader og info i activityDiv
        activityDiv.appendChild(activityHeader);
        activityDiv.appendChild(info);

        // Legg til aktiviteten i containeren
        container.appendChild(activityDiv);
    });
}

function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secondsLeft = seconds % 60;
    return `${hours}t ${minutes}m ${secondsLeft}s`;
}
