// frontend/js/sidebar.js

// Konstant for å kontrollere sidebar:
let openSidebar = null;

// Funksjon for å lage sidebar
function createSidebars() {
    const mainContent = document.getElementById("main-content");

    const leftSidebar = document.createElement('div');
    const rightSidebar = document.createElement('div');
    leftSidebar.id = 'leftSidebar';
    leftSidebar.style.left = '-400px';
    rightSidebar.id = 'rightSidebar';
    rightSidebar.style.right = '-400px';

    mainContent.appendChild(leftSidebar);
    mainContent.appendChild(rightSidebar);

    createSidebarButton('left', 'left-sidebar-btn');
    createSidebarButton('right', 'right-sidebar-btn');

    // document.getElementById("right-sidebar-btn").style.display = 'none';
}

function createSidebarButton(side, id) {
    const button = createSVG("toggle-sidebar-btn",
        "M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3v-3z",
        "4vh", "4vh", "0 0 16 16");

    button.id = id;

    const position = side === 'left' ? 'left' : 'right';
    setPositionToSVG(button, 'fixed', position, '20px', '20px');
    document.getElementById("main-content").appendChild(button);

    // Legg til event listener
    button.addEventListener('click', () => {
        if (side === 'left') {
            toggleLeftSidebar();
        } else {
            toggleRightSidebar();
        }
    });
}

// Funksjon for å åpne og lukke sidebar
function toggleLeftSidebar() {
    const sidebar = document.getElementById('leftSidebar');
    const dataField = document.getElementById('data-field');
    // Når venstre sidebar er skjult (utenfor skjermen)
    if (sidebar.style.left === '-400px') {
        if (openSidebar !== null) {
            toggleRightSidebar();
        }
        sidebar.style.left = '0px';
        openSidebar = 'left';
        document.documentElement.style.setProperty('--margin', '390px');
        dataField.style.marginLeft = '400px';
    } else {
        sidebar.style.left = '-400px';
        openSidebar = null;
        document.documentElement.style.setProperty('--margin', '0px');
        dataField.style.marginLeft = '0px';
    }
}

function toggleRightSidebar() {
    const sidebar = document.getElementById('rightSidebar');
    const dataField = document.getElementById('data-field');
    // Når høyre sidebar er skjult (utenfor skjermen)
    if (sidebar.style.right === '-400px') {
        if (openSidebar !== null) {
            toggleLeftSidebar();
        }
        sidebar.style.right = '0px';
        openSidebar = 'right';
        document.documentElement.style.setProperty('--margin', '390px');
        dataField.style.marginRight = '400px';
    } else {
        sidebar.style.right = '-400px';
        openSidebar = null;
        document.documentElement.style.setProperty('--margin', '0px');
        dataField.style.marginRight = '0px';
    }
}

// Kall funksjonen for å generere sidebar ved lasting av siden
document.addEventListener('DOMContentLoaded', () => {
    createSidebars();
});
