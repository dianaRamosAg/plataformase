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

     if(nivel == 3){
        $("#select_nivel_educativo").empty();
        $("#select_nivel_educativo").append(new Option("Seleccione nivel educativo",0));
        $("#select_nivel_educativo").append(new Option("Media Superior",1));
        $("#select_nivel_educativo").append(new Option("Superior",2));
    }
}
        
   
  

