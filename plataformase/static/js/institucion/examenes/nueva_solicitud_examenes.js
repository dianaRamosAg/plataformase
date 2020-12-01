$(function () {
    $('[class="form-control"]').change(function(){
        if(!validar()) {
            $('#avanzar').attr("disabled", true);
        } else {
            $('#avanzar').attr("disabled", false);
        }
    });
  });



function validar() {
    var categoria = document.getElementById("sel").value;
    var secretario = document.getElementById("selectSecretario").value;
    var nivel = document.getElementById("select_nivel_educativo").value;
    var cct = document.getElementById("select_cct").value;
    var presidente = document.getElementById("selectPresidente").value;
    var vocal = document.getElementById("selectVocal").value;
    var fecha = document.getElementById("fechaexa").value;
    var hoy = new Date();
    var RegExPattern = /^\d{1,2}\/\d{1,2}\/\d{2,4}$/;

    if (categoria == 'Seleccionar' || categoria == 'OTROS') {
        return false;
    } else if (secretario == 'Seleccionar') {
        return false;
    } else if (presidente == 'Seleccionar') {
        return false;
    } else if (vocal == 'Seleccionar') {
        return false;
    }else if (secretario == presidente || secretario == vocal || presidente == vocal) {
        return false;
    } else if(nivel == "0"){
        return false;
    }else if(cct == "0"){
        return false;
    } else return true;

    
}

function otrosOnChange(sel) {
    if (sel.value=="9"){
         divC = document.getElementById("nCuenta");
         divC.style.display = "";

    }else{

         divC = document.getElementById("nCuenta");
         divC.style.display="none";
    }
}
