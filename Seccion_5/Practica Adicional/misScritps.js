
function recomendarActividad() {
    let elementoPresupuesto = document.getElementById("presupuesto");
    let elementoCantidad = document.getElementById("cantidadPersonas");
    let elementoActividades = document.getElementById("actividades");
    let elementoResultado = document.getElementById("recomendacion");

    let presupuesto = Number(elementoPresupuesto.value);
    let cantidad = Number(elementoCantidad.value);
    let actividad = elementoActividades.value;

    let recomendada = "";

    switch (actividad) {
        case "deportes":
            if (presupuesto < 8000) {
                recomendada = "Caminata recreativa";
            } else if (presupuesto < 15000) {
                recomendada = "Alquiler de cancha";
            } else {
                recomendada = "Actividad deportiva especializada";
            }
            break;

        case "entretenimiento":
            if (presupuesto < 8000) {
                recomendada = "Actividad económica";
            } else if (presupuesto <= 15000) {
                recomendada = "Entrada al cine";
            } else {
                recomendada = "Concierto o espectáculo";
            }
            break;

        case "turismo":
            if (presupuesto < 8000) {
                recomendada = "Visita a parque público";
            } else if (presupuesto <= 15000) {
                recomendada = "Tour local";
            } else {
                recomendada = "Excursión de día completo";
            }
            break;

        case "familiares":
            if (presupuesto < 8000) {
                recomendada = "Picnic familiar";
            } else if (presupuesto <= 15000) {
                recomendada = "Salida recreativa";
            } else {
                recomendada = "Parque temático o actividad especial";
            }
            break;
    }

    let descuento = 0;
    let textoDesc = "0%";

    if (cantidad >= 5 && cantidad <= 8) {
        descuento = 10;
        textoDesc = "10%";
    } 
    
    else if (cantidad >= 9) {
        descuento = 15;
        textoDesc = "15%";
    }

    let montoDescuento = (presupuesto * descuento) / 100;
    let presupuestoFinal = presupuesto - montoDescuento;
    

    elementoResultado.innerHTML = 
        "Actividad recomendada: " + recomendada + "<br>" +
        "Cantidad de personas: " + cantidad  +  "<br>" +
        "Porcentaje de descuento aplicado: " + textoDesc + "<br>" +
        "Monto del descuento: ₡" + montoDescuento  + "<br>" +
        "Presupuesto final: ₡" + presupuestoFinal;
}

function reiniciar() {
    document.getElementById("presupuesto").value = "";
    document.getElementById("cantidadPersonas").value = "";
    document.getElementById("actividades").value = "";
    document.getElementById("recomendacion").innerHTML = "---";
}