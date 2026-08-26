function evaluarCompra(cantidadDisponible) {
    let elementoRespuesta = document.
    getElementById("decision");

    let elementoCantidad = document.
    getElementById("textoCantidad");
    let cantidadComprada = elementoCantidad.value;

    if (cantidadComprada <= cantidadDisponible) {
        elementoRespuesta.textContent = "Compraste " + cantidadComprada
        + " hay disponible aun " +
        (cantidadDisponible -
        parseInt(cantidadComprada)).toString();
    }
}
