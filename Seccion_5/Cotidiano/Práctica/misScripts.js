function recomendarPelicula() {
    let elementoEdad = document.getElementById("numeroEdad");
    let elementoGenero = document.getElementById("generoPelicula");
    let elementoRecomendacion = document.getElementById("recomendacion");

    let edad = Number(elementoEdad.value);
    let genero = elementoGenero.value;


    if (elementoEdad.value === "") {
        elementoRecomendacion.textContent = "Ingrese su edad!";
        return;
    }

    let pelicula = "";

    switch (genero) {
        case "drama":
            if (edad < 13) {
                pelicula = "CasaBlanca";
            } 
            else if (edad >= 13 && edad <=15) {
                pelicula = "The Shawshank Redemption";
            }

            else if (edad >=16) {
                pelicula = "Taxi Driverr";   
            }
           

            
            break;

        case "comedia":
            if (edad <13) {
            pelicula = "Back to the Future"
            }

             else if (edad >= 13 && edad <=15) {
            pelicula = "The Truman Show"
            }

            else if (edad >=16) {
            pelicula = "The Wolf of Wall Street"
            }
            break;

        case "musical":
            if (edad < 13) {
            pelicula = "La La Land"
            }
            else if (edad >= 13 && edad <=15) {
            pelicula = "Les Miserables"   
            }

            else if (edad >=16) {
            pelicula = "The Rocky Horror Picture Show"
            }
            break;

         case "crimen":
            if (edad <13) {
            pelicula = "No hay opciones"
            }

            else if (edad >= 13 && edad <=15) {
            pelicula = "El Secreto de sus Ojos"
            }

            else if (edad >=16)
            pelicula = "The Godfather"
    
        default:
            break;
    }   

    elementoRecomendacion.textContent = `Pelicula Recomendada: ${pelicula}`;

}


