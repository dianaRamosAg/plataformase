document.addEventListener("DOMContentLoaded", cargarListeners, false);

function updateNivelEducativo(){
    var selectNivelEducativo = document.getElementById("select_nivel_educativo");
    $.ajax({
        url: '/SETyRS/institucion/Updsolicitud/sinodal/26/',
        headers:{ "X-CSRFToken": $('meta[name="_token"]').attr('content') },
        data: 
            {
                idSoliSinod: idSolicitud,
                nuevoNivel: $("#select_nivel_educativo option:selected").val()
            },
        type: 'POST',
        async: true,
        dataType: "json",
        success:function(response){
        }
    })
};

function cargarListeners() { 
    var selectNivelEducativo = document.getElementById("select_nivel_educativo");
    selectNivelEducativo.addEventListener("change",updateNivelEducativo,false);

    $.ajax({
        url: '/SETyRS/institucion/examenes/get/nivelCCT',
        method: 'GET',
        data:
            {
                'cct':cct,
            },
            dataType: "json",
            success:function(response){
               var centroTrabajo = JSON.parse(response);
               var nivel = centroTrabajo[0]["fields"]["nivel_educativo"];

               $("#select_nivel_educativo").empty();
               $("#select_nivel_educativo").append(new Option("Seleccione nivel educativo",0));

               if(nivel == 3){
                    $("#select_nivel_educativo").append(new Option("Media Superior",1));
                    $("#select_nivel_educativo").append(new Option("Superior",2));
               }
               else if(nivel == 2){
                $("#select_nivel_educativo").append(new Option("Superior",2));
               }
               else if(nivel == 1){
                $("#select_nivel_educativo").append(new Option("Media Superior",1));
               }
            }
           
    })
  }

