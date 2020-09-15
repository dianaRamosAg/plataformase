
function cargarListeners() { 
    var btnC = document.getElementById("btnContinuar");
    btnC.addEventListener("click",continuarSoli,false);
};

function continuarSoli(){
    console.log("Entra a la funcion");
    var divContainer = document.getElementById("buttonContainer");

    divContainer.innerHTML ="";
    //creamos el boton de cargando...
    var creandoBoton = document.createElement("button");
    creandoBoton.className="btn btn-primary mt-3";
    creandoBoton.innerHTML="Guardando archivos..."
    creandoBoton.disabled=true;
    //creamos el span para que gire
    var spanBoton = document.createElement("span");
    spanBoton.className="spinner-border spinner-border-sm";

    //agregamos el span al boton y el boton al div contenedor
    creandoBoton.appendChild(spanBoton);
    divContainer.appendChild(creandoBoton);

    //Depués de haber agregado el botón, enviamos el form para crear la solicitud

    setTimeout(function(){ console.log("continuar") }, 4000);
    
};

  document.addEventListener("DOMContentLoaded", cargarListeners, false);