function mostrarBA() {
    checkba = document.getElementById("checkBA");
    ba = document.getElementById("BA")
    if (checkba.checked) {
        ba.style.display='block'
        document.getElementById("date").value="";
        document.getElementById("institucion").value="";
    } else {
        var select, table;
    select = $('#select').val();
    table = document.getElementById("solicitudes");
    tr = table.getElementsByTagName("tr");

    console.log(select)

    if(select==1){
        for(i=0;i<tr.length;i++) {
            tr[i].style.display = "";
        }
    } else if(select==2) {
        for(i=0;i<tr.length;i++) {
            td = tr[i].getElementsByTagName("td")[2];
            if(td) {
                if (td.innerHTML.toUpperCase() == "PENDIENTE") {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    } else if(select==3) {
        for(i=0;i<tr.length;i++) {
            td = tr[i].getElementsByTagName("td")[2];
            if(td) {
                if (td.innerHTML.toUpperCase() == "APROBADA") {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        } 
    } else if(select==4) {
        for(i=0;i<tr.length;i++) {
            td = tr[i].getElementsByTagName("td")[2];
            if(td) {
                if (td.innerHTML.toUpperCase() == "RECHAZADA") {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        } 
    } 
        ba.style.display='none'
    }
}

function buscarSolicitud(){
    var select, table;
    select = $('#select').val();
    table = document.getElementById("solicitudes");
    tr = table.getElementsByTagName("tr");

    console.log(select)

    if(select==1){
        for(i=0;i<tr.length;i++) {
            tr[i].style.display = "";
        }
    } else if(select==2) {
        for(i=0;i<tr.length;i++) {
            td = tr[i].getElementsByTagName("td")[2];
            if(td) {
                if (td.innerHTML.toUpperCase() == "PENDIENTE") {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    } else if(select==3) {
        for(i=0;i<tr.length;i++) {
            td = tr[i].getElementsByTagName("td")[2];
            if(td) {
                if (td.innerHTML.toUpperCase() == "APROBADA") {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        } 
    } else if(select==4) {
        for(i=0;i<tr.length;i++) {
            td = tr[i].getElementsByTagName("td")[2];
            if(td) {
                if (td.innerHTML.toUpperCase() == "RECHAZADA") {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        } 
    } 
}

function buscar() {
    var filter, table, input, date, options, fecha, select;
    select = $('#select').val();
    input = $('#institucion').val();
    date = $('#date').val();
    arrayfecha = date.split("-");
    fecha = new Date(arrayfecha[0],arrayfecha[1]-1,arrayfecha[2]);
    options = { year: 'numeric', month: 'long', day: 'numeric' };
    fecha = fecha.toLocaleDateString("es-ES", options).toUpperCase();
    filter = input.toUpperCase();
    table = document.getElementById("solicitudes");
    tr = table.getElementsByTagName("tr");

    if(fecha != "INVALID DATE") {
        for(i=0;i<tr.length;i++) {
            td = tr[i].getElementsByTagName("td")[1];
            td2 = tr[i].getElementsByTagName("td")[3];
            if(td && td2) {
                if (td.innerHTML.toUpperCase().indexOf(filter) > -1 && td2.innerHTML.toUpperCase() == fecha) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    } else {
        for(i=0;i<tr.length;i++) {
            td = tr[i].getElementsByTagName("td")[1];
            if(td) {
                if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }
}