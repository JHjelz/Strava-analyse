// frontend/js/sidebar/style.js

// Generere sidebar-innhold:
function generateLeftContent() {
    const container = createDiv();

    const button = createSVG('toggle-sidebar-btn',
        'M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z',
        '4vh', '4vh', '0 0 16 16');
    button.addEventListener('click', toggleLeftSidebar);
    
    const title = document.createElement('h2');
    title.textContent = 'Strava-data';

    const info = document.createElement('p');
    info.textContent = 'Legg inn nødvendig informasjon for å koble til Strava';
    
    const i1 = document.createElement('p');
    i1.classList.add('bold');
    i1.textContent = "Client ID:";

    const in1 = createInputField("Client ID", "idInput");
    in1.addEventListener('click', () => {
        removeWarning("idInput");
    })
    
    const i2 = document.createElement('p');
    i2.classList.add('bold');
    i2.textContent = "Client Secret:";
    
    const in2 = createInputField("Client Secret", "secretInput");
    in2.addEventListener('click', () => {
        removeWarning("secretInput");
    })
    
    const i3 = document.createElement('p');
    i3.classList.add('bold');
    i3.textContent = "Refresh Token:";
    
    const in3 = createInputField("Refresh Token", "refreshInput");
    in3.addEventListener('click', () => {
        removeWarning("refreshInput");
    })

    const submit = createButton("Hent data", "submitStrava", get_strava_data);

    container.appendChild(button);
    container.appendChild(title);
    container.appendChild(info);
    container.appendChild(i1);
    container.appendChild(in1);
    container.appendChild(i2);
    container.appendChild(in2);
    container.appendChild(i3);
    container.appendChild(in3);

    document.getElementById('leftSidebar').appendChild(container);
    document.getElementById('leftSidebar').appendChild(submit);
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
