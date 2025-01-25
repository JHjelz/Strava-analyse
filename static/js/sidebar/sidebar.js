// static/js/sidebar/sidebar.js

// Generere sidebars:
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
}

// Generere knapper for å åpne sidebars:
function createSidebarButton(side, id) {
    const button = createSVG("toggle-sidebar-btn",
        "M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3v-3z",
        "6vh", "6vh", "0 0 16 16");

    button.id = id;

    const position = side === 'left' ? 'left' : 'right';
    setPositionToSVG(button, 'fixed', position, '55px', '40px');
    document.getElementById("main-content").appendChild(button);

    button.addEventListener('click', () => {
        if (side === 'left') {
            toggleLeftSidebar();
        } else {
            toggleRightSidebar();
        }
    });
}
