// frontend/js/utils/dom.js

// Genererer div:
function createDiv() {
    const container = document.createElement('div');
    container.classList.add('flex-container');
    return container;
}

// Genererer knapper:
function createButton(text, id, onClickHandler) {
    const button = document.createElement('button');
    button.id = id;
    button.textContent = text;
    button.addEventListener('click', onClickHandler);
    return button;
}

// Genererer input-felt:
function createInputField(text, id) {
    const input = document.createElement('input');
    input.id = id;
    input.classList.add('input');
    input.placeholder = text;
    return input;
}

// Genererer SVG-element:
function createSVG(iconClass, iconPath, width, height, viewbox) {
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("class", iconClass);
    svg.setAttribute("width", width);
    svg.setAttribute("height", height);
    svg.setAttribute("fill", "currentColor");
    svg.setAttribute("viewBox", viewbox);

    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", iconPath);
    svg.appendChild(path);

    return svg;
}

// Plasserer SVG-element rett sted:
function setPositionToSVG(svg, pos, dir, val, bottom) {
    svg.style.position = pos;
    if (dir === "left") {
        svg.style.left = val;
    }
    else if (dir === "right") {
        svg.style.right = val;
    }
    svg.style.bottom = bottom;
}

// Fjerner 'warning'-status:
function removeWarning(id) {
    const element = document.getElementById(id)
    
    if (element.classList.contains("warning")) {
        element.classList.remove("warning");
    }
    element.value = "";
}
