// static/js/elements/progressBar.js

// Dynamisk opprettelse av vventeboks og progress bar::
function createLoadingModal() {
    const modal = document.createElement("div");
    modal.id = "loadingModal";
    modal.style.position = "fixed";
    modal.style.top = "0";
    modal.style.left = "0";
    modal.style.width = "100%";
    modal.style.height = "100%";
    modal.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    modal.style.display = "flex";
    modal.style.justifyContent = "center";
    modal.style.alignItems = "center";
    modal.style.zIndex = "1000";

    const content = document.createElement("div");
    content.style.backgroundColor = "#fff";
    content.style.padding = "20px";
    content.style.borderRadius = "10px";
    content.style.textAlign = "center";
    content.style.width = "300px";
    content.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.2)";

    const title =  document.createElement("h2");
    title.innerText = "Laster data...";
    content.appendChild(title)

    const progressBarContainer = document.createElement("div");
    progressBarContainer.style.width = "100%";
    progressBarContainer.style.backgroundColor = "#f3f3f3";
    progressBarContainer.style.borderRadius = "5px";
    progressBarContainer.style.marginTop = "20px";
    progressBarContainer.style.overflow = "hidden";

    const progressBar = document.createElement("div");
    progressBar.id = "progressBarFill";
    progressBar.style.width = "0%";
    progressBar.style.height = "20px";
    progressBar.style.backgroundColor = "#4caf50";
    progressBar.style.transition = "width 0.2s";
    progressBarContainer.appendChild(progressBar);

    const progressText = document.createElement("div");
    progressText.id = "progressText";
    progressText.style.marginTop = "10px";
    progressText.style.fontSize = "16px";
    progressText.style.fontWeight = "bold";
    progressText.innerText = "0%";

    content.appendChild(progressBarContainer);
    content.appendChild(progressText);
    modal.appendChild(content);

    document.body.appendChild(modal);

    setupProgressWebSocket();
}

// Fjern venteboksen fra DOM:
function removeLoadingModal() {
    const modal = document.getElementById("loadingModal");
    if (modal) {
        modal.remove();
    }
}

// Oppdater progresjon:
function updateProgress(percentage) {
    const progressBarFill = document.getElementById("progressBarFill");
    const progressText = document.getElementById("progressText");

    if (progressBarFill && progressText) {
        progressBarFill.style.width = `${percentage}%`;
        progressText.innerText = `${percentage}%`;
    }
}

// Koble til WebSocket for progresjonsoppdateringer
function setupProgressWebSocket() {
    const socket = io();

    socket.on('progress', (data) => {
        if (data && data.progress !== undefined) {
            updateProgress(data.progress);
        }
    });
}
