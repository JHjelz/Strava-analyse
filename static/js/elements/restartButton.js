// static/js/elements/restartButton.js

// Restarter siden:
function resetPage() {
    location.reload();
}

function createRestartButton() {
    const button = document.createElement("div");
    button.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="6vh" height="6vh" viewBox="0 0 16 16">
        <path fill="white" fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2z"/>
        <path fill="white" d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466"/>
    </svg>
    `;
    button.id = "restartButton";
    button.className = "restart-btn";
    button.style.position = "fixed";
    button.style.left = "55px";
    button.style.bottom = "40px";
    button.addEventListener("click", () => {
    resetPage();
    });
    document.getElementById("main-content").appendChild(button);
}