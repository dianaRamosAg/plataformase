
function cargarListeners() { 
    var btnC = document.getElementById("btnContinuar");
    btnC.addEventListener("click",continuarSoli,false);
};

$('#confirmacion').on('hidden.bs.modal', function () {
            location.reload();
})

function continuarSoli(){
    var divContainer = document.getElementById("buttonContainer");

    if($("#select_nivel_educativo option:selected").val() != 0){
        divContainer.innerHTML ="";
        //creamos el boton de cargando...
        var creandoBoton = document.createElement("button");
        creandoBoton.className="btn btn-primary mt-3";
        creandoBoton.innerHTML="Agregando sinodales..."
        creandoBoton.disabled=true;
        //creamos el span para que gire
        var spanBoton = document.createElement("span");
        spanBoton.className="spinner-border spinner-border-sm";

        //agregamos el span al boton y el boton al div contenedor
        creandoBoton.appendChild(spanBoton);
        divContainer.appendChild(creandoBoton);

        $('#confirmacion').modal('toggle');
        $('#confirmacion').modal('show');
    }
    else{
        Swal.fire({
            title: 'Por favor seleccione un nivel educativo',
            text: 'Es necesario seleccionar un nivel educativo para la solicitud',
            confirmButtonColor: '#17A2B8',
            confirmButtonText: 'Entendido',
        }).then((result) => {

        })
    }
};


  document.addEventListener("DOMContentLoaded", cargarListeners, false);