// frontend/js/sidebar/style.js

// Generere sidebar-innhold:
function generateLeftContent() {
    const container = createDiv();

    const button = createSVG('toggle-sidebar-btn',
        'M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z',
        '4vh', '4vh', '0 0 16 16');
    button.addEventListener('click', toggleLeftSidebar);
    
    const title = document.createElement('h2');
    title.innerText = 'Velkommen!';

    container.appendChild(button);
    container.appendChild(title);

    document.getElementById('leftSidebar').appendChild(container);
}

// Generere sidebar-innhold:
function generateRightContent() {
    const container = createDiv();

    const button = createSVG('toggle-sidebar-btn',
        'M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z',
        '4vh', '4vh', '0 0 16 16');
    button.addEventListener('click', toggleRightSidebar);
    
    const title = document.createElement('h2');
    title.innerText = 'Velkommen!';

    container.appendChild(button);
    container.appendChild(title);

    document.getElementById('rightSidebar').appendChild(container);
}
