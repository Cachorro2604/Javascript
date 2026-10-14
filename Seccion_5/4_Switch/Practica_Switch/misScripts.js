function consultarPrecio() {
    let elementoFruta = document.getElementById("numeroFruta");
    let fruta = elementoFruta.value.toLowerCase().trim();
    
    let precio;

    switch (fruta) {
        case "manzana":
            precio = 15;
            break;
        case "naranja":
            precio = 20;
            break;
        case "banana":
            precio = 25;
            break;
        default:
            precio = null;
            break;
    }

    if (precio !== null) {
        alert("El precio de la fruta " + fruta + " es: " + precio);
    } else {
        alert("Fruta no encontrada. Intente con Manzana, Naranja o Banana.");
    }
}
