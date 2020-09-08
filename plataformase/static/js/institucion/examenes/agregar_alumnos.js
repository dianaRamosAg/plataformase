// esta funcion obtiene los datos del alumno para ponerlos en ls campos de la ventana modal para la edición
function editAlumno(obj, obj2, obj3, obj4) {
    var id = obj;
    var no_certificado = obj2;
    var nom = obj3;
    var curp = obj4;
    $("#nombre").val(nom)
    $("#cert").val(no_certificado)
    $("#curp").val(curp)
    $("#idAlumn").val(id);
}

//esta funcion obtiene el id del alumno y lo pone en un input invisible al usuario, 
//luego este valor es mandado en el post para ejecutar la eliminacion del alumno
function deleteAlumno(obj) {
    var id = obj;
    $("#idAl").val(id);
}