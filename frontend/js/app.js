// frontend/js/app.js

// Funksjon for å lage sidebar
function createSidebar() {
    const sidebar = document.createElement('div');
    sidebar.id = 'sidebar';

    // Opprett knappene
    const getDataBtn = createButton('Last ned data fra Strava', 'get-data-btn', getData);
    const analyzeBtn = createButton('Analyser data', 'analyze-btn', analyzeData);
    analyzeBtn.style.display = 'none'; // Skjult som standard
    const resetBtn = createButton('Restart', 'reset-btn', resetApp);

    // Legg knappene til sidebar
    sidebar.appendChild(getDataBtn);
    sidebar.appendChild(analyzeBtn);
    sidebar.appendChild(resetBtn);

    // Legg sidebar til main-content
    document.getElementById("main-content").appendChild(sidebar);
}

// Hjelpefunksjon for å lage en knapp
function createButton(text, id, onClickHandler) {
    const button = document.createElement('button');
    button.id = id;
    button.textContent = text;
    button.addEventListener('click', onClickHandler);
    return button;
}

// Funksjoner for knappene
function getData() {
    console.log('Last ned data fra Strava');
    // Legg til logikk for nedlasting av data
}

function analyzeData() {
    console.log('Analyserer data');
    // Legg til analysefunksjonalitet
}

function resetApp() {
    console.log('App restartet');
    // Logikk for å nullstille appen
}

// Funksjon for å åpne og lukke sidebar
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar.style.left === '-300px') {
        sidebar.style.left = '0';
    } else {
        sidebar.style.left = '-300px';
    }
}

// Funksjon for å restarte siden
function resetPage() {
    location.reload();
}

// Kall funksjonen for å generere sidebar ved lasting av siden
document.addEventListener('DOMContentLoaded', () => {
    createSidebar();
});
