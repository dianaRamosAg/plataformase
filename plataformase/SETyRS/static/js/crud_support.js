/*
en este archivo se encuentran las funciones de soporte para las acciones de CRUD en las paginas de agregar sinodales,
agregar documentos, agregar alumno, agregar documentos del alumno.
*/

//Plantilla: agregar_documentos_sinodal.html ------------------------------------------------------------------------------
/* 
esta funcion recibe el id del sinodal y se lo asigna al input #idS para
agregar los documentos al sinodal correspondiente
*/
function getID(id) {
    $("#idS").val(id);
}

/*
esta funcion recibe el id del sinodal, url del curriculum y url de la cedula para mostrar al usuario los valores o archivos
que han sido subidos al sistema mediante la modal de editar y poder hacer una actualizacion de documentos si se requiere
*/
function getIdEdit(id, curr, ced) {
    $("#idSEd").val(id);
    $("#curr").val(curr);
    $("#ced").val(ced);
}
//fin de pagina

//Plantilla: agregar_sinodal.html ---------------------------------------------------------------------------------------
/* 
esta funcion recibe los datos del sinodal para poder ser mostrados en la modal de editar sinodal y poder ser actualizados
en caso de ser necesarios
*/
function editSinodal(id,nombre_sinodal, curp, rfc, grado_academico) {
    $("#idSino").val(id);
    $("#nombre_edit").val(nombre_sinodal);
    $("#curp_edit").val(curp);
    $("#rfc_edit").val(rfc);
    $("#grado_edit").val(grado_academico);
}

//esta funcion recibe el id del sinodal y se lo asigna a un input no visible para poder hacer el delete en la BD
function deleteSinodal(id) {
    $("#idSin").val(id);
}