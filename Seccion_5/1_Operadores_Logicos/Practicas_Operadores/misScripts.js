function calcular(){
   
    let elemento1 = document.getElementById("textoNumero1");
    let elemento2 = document.getElementById("textoNumero2");

  
    let numero1 = Number(elemento1.value);
    let numero2 = Number(elemento2.value);

    
    let comparacion = numero1 > numero2;

    
    let elementoRespuesta = document.getElementById("resultado");
    elementoRespuesta.textContent = comparacion;
}
