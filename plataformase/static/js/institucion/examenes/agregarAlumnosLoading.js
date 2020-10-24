function cargarListeners() { 
    var btnC = document.getElementById("btnContinuar");
    btnC.addEventListener("click",continuarSoli,false);
    console.log("están cocachis");
};



function continuarSoli(){
    var divContainer = document.getElementById("buttonContainer");

    divContainer.innerHTML ="";
    //creamos el boton de cargando...
    var creandoBoton = document.createElement("button");
    creandoBoton.className="btn btn-primary mt-3";
    creandoBoton.innerHTML="Agregando alumnos..."
    creandoBoton.disabled=true;
    //creamos el span para que gire
    var spanBoton = document.createElement("span");
    spanBoton.className="spinner-border spinner-border-sm";

    //agregamos el span al boton y el boton al div contenedor
    creandoBoton.appendChild(spanBoton);
    divContainer.appendChild(creandoBoton);
    
    $('#confirmacion').modal('toggle');
    $('#confirmacion').modal('show');

    $('#confirmacion').on('hidden.bs.modal', function () {
        location.reload();
    })

    $("#btnContinuarF").click(function(){
        $(this).prop("disabled",true);
        $("#FormGuardarAlumnos").submit();
    })
};

  document.addEventListener("DOMContentLoaded", cargarListeners, false);