function obtenerNotasDesdeHTML() {
    const elementos = document.querySelectorAll("ul li");
    return Array.from(elementos).map(li => parseFloat(li.textContent));
}

function calcularPromedio() {
    const notas = obtenerNotasDesdeHTML();
    const suma = notas.reduce((acumulado, actual) => acumulado + actual, 0);
    const promedio = suma / notas.length;
    alert(`El promedio es: ${promedio.toFixed(1)}`);
}

function notaALTA() {
    const notas = obtenerNotasDesdeHTML();
    const maxima = Math.max(...notas);
    console.log(notaALTA)
}

function consultarAplazo() {
    const notas = obtenerNotasDesdeHTML();
    const tieneAplazados = notas.some(nota => nota < 4);
    const resultado = tieneAplazados ? "Sí, hay aplazos." : "No, no hay aplazos.";
    alert(resultado);
}
