let notas = [7, 4, 8, 9, 6];

function listarNotas() {
    let lugar = document.getElementById("mi-lista");
    lugar.innerHTML = "";
    
    for (let nota of notas) {
        let elemento = document.createElement("li");
        elemento.textContent = nota;
        lugar.appendChild(elemento);
    }
}

function calcularPromedio() {
    let sumaPromedio = 0;
    for (let i = 0; i < 5; i++) {
        sumaPromedio = sumaPromedio + notas[i];
    }
    let resultadoPromedio = sumaPromedio / 5;
    document.getElementById("res-promedio").textContent = resultadoPromedio;
}

function notaMasAlta() {
    let notaMayor = notas[0];
    for (let i = 1; i < 5; i++) {
        if (notas[i] > notaMayor) {
            notaMayor = notas[i];
        }
    }
    document.getElementById("res-alta").textContent = notaMayor;
}

function hayAplazados() {
    let respuestaAplazado = "No";
    for (let i = 0; i < 5; i++) {
        if (notas[i] < 4) {
            respuestaAplazado = "Sí";
            break;
        }
    }
    document.getElementById("res-aplazado").textContent = respuestaAplazado;
}