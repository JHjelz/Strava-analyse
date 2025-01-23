// frontend/js/sidebar/logic.js

// Kontrollere åpne sidebars:
let openSidebar = null;

// Ta i bruk sidebars:
function toggleLeftSidebar() {
    const sidebar = document.getElementById('leftSidebar');
    const dataField = document.getElementById('data-field');
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
