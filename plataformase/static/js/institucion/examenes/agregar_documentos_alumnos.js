//obtiene el id del alumno y se lo proporciona a la ventana modal para agregar sus documentos
function getID(id) {
    $("#id").val(id);
}

//obtiene el id y archivos del alumno para mostrarlos en la ventana modal de editar, esta funcion
// solo se ejecuta cuando ya se han subido archivos previamente
function getIdEdit(id, cert, cotejo, control, recibo) {
    $("#idEd").val(id);
    $("#certi").val(cert);
    $("#cotejo").val(cotejo);
    $("#control").val(control);
    $("#recibo").val(recibo);
}

//esta funcion es para reabrir la ventana modal de editar cuando se cierra la de visualizar archivos
function openAgainEditModal() {
    $('#editDocs').modal('show');
}

$(document).ready(function()
	{
	   $("#error").modal("show");
	});