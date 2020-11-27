var btnGuardar = "";

function cargarListeners() { 
    var btnContinuar = document.getElementById("btnContinuar");
    btnContinuar.addEventListener("click",continuarSoli,false);
    btnGuardar = document.getElementById("btnGuardar");
};




//Listeners para evaluar que ambos archivos se hayan subido antes de activar el botón de guardar
$("#id_curriculum").change(function(){
    if($("#id_cedula").val()){
        $("#btnGuardar").prop("disabled",false)
    }
})

$("#id_cedula").change(function(){
    if($("#id_curriculum").val()){
        $("#btnGuardar").prop("disabled",false)
    }
})
// Fin listeners archivos
   

//Listener btnGuardar para desactivar al dar click
$("#btnGuardar").click(function(){
    $(this).prop("disabled",true);
    $("#formGuardarDocs").submit();
})

$("#btnContinuar").click(function(){
    $(this).prop("disabled",true);
    $("#agregarDocumentos").submit();
})


//Cambiamos el botón al presionarlo una vez
function continuarSoli(){
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
    
};

  document.addEventListener("DOMContentLoaded", cargarListeners, false);