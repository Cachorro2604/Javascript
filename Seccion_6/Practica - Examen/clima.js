function obtenerGradosDesdeHTML() {
    const elementos = document.querySelectorAll("ul li");
    return Array.from(elementos).map(li => parseFloat(li.textContent));
}

function calcularPromedio(){
    const grados = obtenerGradosDesdeHTML();
    const suma = grados.reduce((acumulado, actual) => acumulado + actual, 0);
    const promedio = suma / grados.length;
    
    const divResultado = document.getElementById("promTemp");
    divResultado.innerHTML = `<strong>${promedio.toFixed(2)}°</strong>`;
}


function calcularMax() {
    const grados = obtenerGradosDesdeHTML();
    
    if (grados.length === 0) return;

    const maxima = Math.max(...grados);
    
    const divResultadoMax = document.getElementById("promMax");
    divResultadoMax.innerHTML = `<strong>${maxima}°</strong>`;
}

function calcularFrio() {
    const grados = obtenerGradosDesdeHTML();
    const gradoFrio = grados.some(g => g < 20);
    const resultadoFrio = gradoFrio ? "El día más frío es de 20° " : "No hay días fríos";
    const divResultadoFrio = document.getElementById("promFrio");
    divResultadoFrio.innerHTML = `<strong>${resultadoFrio}</strong>`;
}


