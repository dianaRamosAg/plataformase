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
    var categoria = document.getElementById("selectCategoria").value;
    var secretario = document.getElementById("selectSecretario").value;
    var presidente = document.getElementById("selectPresidente").value;
    var vocal = document.getElementById("selectVocal").value;

    if (categoria == 'Seleccionar') {
        return false;
    } else if (secretario == 'Seleccionar') {
        return false;
    } else if (presidente == 'Seleccionar') {
        return false;
    } else if (vocal == 'Seleccionar') {
        return false;
    }else if (secretario == presidente || secretario == vocal || presidente == vocal) {
        return false;
    } else return true;
}