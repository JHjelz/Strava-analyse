// frontend/js/app.js

// Funksjon for å lage header
function createHeader() {
    const header = document.createElement("header");

    // Lag venstre SVG
    const leftSVG = createSVG("icon-left",
        "M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0ZM3.668 2.501l-.288.646a.847.847 0 0 0 1.479.815l.245-.368a.809.809 0 0 1 1.034-.275.809.809 0 0 0 .724 0l.261-.13a1 1 0 0 1 .775-.05l.984.34c.078.028.16.044.243.054.784.093.855.377.694.801-.155.41-.616.617-1.035.487l-.01-.003C8.274 4.663 7.748 4.5 6 4.5 4.8 4.5 3.5 5.62 3.5 7c0 1.96.826 2.166 1.696 2.382.46.115.935.233 1.304.618.449.467.393 1.181.339 1.877C6.755 12.96 6.674 14 8.5 14c1.75 0 3-3.5 3-4.5 0-.262.208-.468.444-.7.396-.392.87-.86.556-1.8-.097-.291-.396-.568-.641-.756-.174-.133-.207-.396-.052-.551a.333.333 0 0 1 .42-.042l1.085.724c.11.072.255.058.348-.035.15-.15.415-.083.489.117.16.43.445 1.05.849 1.357L15 8A7 7 0 1 1 3.668 2.501Z",
        "11vh", "11vh", "0 0 16 16");

    // Lag overskrift
    const h1 = document.createElement("h1");
    h1.textContent = "Strava-analyse";

    // Lag høyre SVG
    const rightSVG = createSVG("icon-right",
        "M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0ZM1.612 10.867l.756-1.288a1 1 0 0 1 1.545-.225l1.074 1.005a.986.986 0 0 0 1.36-.011l.038-.037a.882.882 0 0 0 .26-.755c-.075-.548.37-1.033.92-1.099.728-.086 1.587-.324 1.728-.957.086-.386-.114-.83-.361-1.2-.207-.312 0-.8.374-.8.123 0 .24-.055.318-.15l.393-.474c.196-.237.491-.368.797-.403.554-.064 1.407-.277 1.583-.973.098-.391-.192-.634-.484-.88-.254-.212-.51-.426-.515-.741a6.998 6.998 0 0 1 3.425 7.692 1.015 1.015 0 0 0-.087-.063l-.316-.204a1 1 0 0 0-.977-.06l-.169.082a1 1 0 0 1-.741.051l-1.021-.329A1 1 0 0 0 11.205 9h-.165a1 1 0 0 0-.945.674l-.172.499a1 1 0 0 1-.404.514l-.802.518a1 1 0 0 0-.458.84v.455a1 1 0 0 0 1 1h.257a1 1 0 0 1 .542.16l.762.49a.998.998 0 0 0 .283.126 7.001 7.001 0 0 1-9.49-3.409Z",
        "11vh", "11vh", "0 0 16 16");

    // Sett sammen headeren
    header.appendChild(leftSVG);
    header.appendChild(h1);
    header.appendChild(rightSVG);

    // Legg til headeren i DOM-en
    document.getElementById("header-container").appendChild(header);
}

// Funksjon for å lage SVG-element
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

// Hjelpefunksjon for å lage en knapp
function createButton(text, id, onClickHandler) {
    const button = document.createElement('button');
    button.id = id;
    button.textContent = text;
    button.addEventListener('click', onClickHandler);
    return button;
}

// Funksjon for å restarte siden
function resetPage() {
    location.reload();
}

// Kall funksjonen for å generere header ved lasting av siden
document.addEventListener('DOMContentLoaded', () => {
    createHeader();
});
