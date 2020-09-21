var RIT = false;
var CCT = "";

$("#select_cct").on('change',function(){
    CCT = $("#select_cct").children("option:selected").val();
    $.ajax({
        url: '/SETyRS/institucion/examenes/get/nivelCCT',
        data:
            {
                'cct':$("#select_cct").children("option:selected").val(),
            },
            dataType: "json",
            success:function(response){
               var centroTrabajo = JSON.parse(response);
               var nivel = centroTrabajo[0]["fields"]["nivel_educativo"];

               $("#select_nivel_educativo").empty();
               $("#select_nivel_educativo").append(new Option("Seleccione nivel educativo"),"0");

               if(nivel == 3){
                    $("#select_nivel_educativo").append(new Option("Media Superior"),"1");
                    $("#select_nivel_educativo").append(new Option("Superior"),"2");
               }
               else if(nivel == 2){
                $("#select_nivel_educativo").append(new Option("Superior"),"2");
               }
               else if(nivel == 1){
                $("#select_nivel_educativo").append(new Option("Media Superior"),"1");
               }
            }
           
    })
    if($("#sel option:selected").val() == "9"){getReglamento(CCT)}
});

$("#sel").on("change",function(){
    if($("#sel").children("option:selected").val() == "9" && CCT != "" ){
        getReglamento(CCT);
    }
})


function getReglamento(cct_selected){
    $.ajax({
        url: '/SETyRS/institucion/examenes/get/RIT',
        data: { 'cct': cct_selected},
        dataType: "json",
        success:function(response){
            if(JSON.parse(response).length == 0){
                showModal();
            }
        }
    })
}

function showModal(){
            if($("#select_cct").children("option:selected").val() != "0"){
                var cct = $("#select_cct").children("option:selected").val()
                $('#agregarDocumentoModal').modal('show');
                $("#centroTrabajo").val(cct);
            }

        $("#documentoPendiente").on("change",function(){
            $("#btnGuardar").removeAttr('disabled');
        })

        $('#agregarDocumentoModal').on('hidden.bs.modal', function () {
            location.reload();
        })
    }

function cargarListeners() { 
    var btnNS = document.getElementById("avanzar");
    btnNS.addEventListener("click",creandoSoli,false);
};



function creandoSoli(){
    var btnNS = document.getElementById("avanzar");
    var divContainer = document.getElementById("buttonContainer");

    divContainer.innerHTML ="";
    //creamos el boton de cargando...
    var creandoBoton = document.createElement("button");
    creandoBoton.className="btn btn-primary mt-3";
    creandoBoton.innerHTML="Creando solicitud..."
    creandoBoton.disabled=true;

    //creamos el span para que gire
    var spanBoton = document.createElement("span");
    spanBoton.className="spinner-border spinner-border-sm";

    //agregamos el span al boton y el boton al div contenedor
    creandoBoton.appendChild(spanBoton);
    divContainer.appendChild(creandoBoton);

    //Depués de haber agregado el botón, enviamos el form para crear la solicitud
    document.getElementById("enviarSolicitud").submit();
};

  document.addEventListener("DOMContentLoaded", cargarListeners, false);