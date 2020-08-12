document.addEventListener("DOMContentLoaded", cargarListeners, false);

function updateNivelEducativo(){
    var selectNivelEducativo = document.getElementById("select_nivel_educativo");
    $.ajax({
        url: '/SETyRS/institucion/Updsolicitud/sinodal/26/',
        headers:{ "X-CSRFToken": $('meta[name="_token"]').attr('content') },
        data: 
            {
                idSoliSinod: idSolicitud,
                nuevoNivel: selectNivelEducativo.value
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
  }

