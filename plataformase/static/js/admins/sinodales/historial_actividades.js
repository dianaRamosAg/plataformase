function mostrarBA() {
    checkba = document.getElementById("checkBA");
    ba = document.getElementById("BA")
    if (checkba.checked) {
        ba.style.display='block'
        document.getElementById("nombre").value="";
        document.getElementById("rfc").value="";
        document.getElementById("institucion").value="";
    } else {
        document.getElementById("nombre").value="";
        document.getElementById("rfc").value="";
        document.getElementById("institucion").value="";
        var filter, table, inst, name, rfc, select;
    //select = $('#select').val();
    name = $('#nombre').val().toUpperCase();
    inst = $('#institucion').val().toUpperCase();
    rfc = $('#rfc').val().toUpperCase();
    table = document.getElementById("sinodales");
    tr = table.getElementsByTagName("tr");

    for(i=0;i<tr.length;i++) {
        td1 = tr[i].getElementsByTagName("td")[1];
        td2 = tr[i].getElementsByTagName("td")[2];
        td3 = tr[i].getElementsByTagName("td")[3];
        if(td1) {
            if (td1.innerHTML.toUpperCase().indexOf(name) > -1 && td2.innerHTML.toUpperCase().indexOf(rfc) > -1 && td3.innerHTML.toUpperCase().indexOf(inst) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
        ba.style.display='none'
    }
}

function buscar() {
    var filter, table, inst, name, rfc, select;
    //select = $('#select').val();
    name = $('#nombre').val().toUpperCase();
    inst = $('#institucion').val().toUpperCase();
    rfc = $('#rfc').val().toUpperCase();
    table = document.getElementById("sinodales");
    tr = table.getElementsByTagName("tr");

    for(i=0;i<tr.length;i++) {
        td1 = tr[i].getElementsByTagName("td")[1];
        td2 = tr[i].getElementsByTagName("td")[2];
        td3 = tr[i].getElementsByTagName("td")[3];
        if(td1) {
            if (td1.innerHTML.toUpperCase().indexOf(name) > -1 && td2.innerHTML.toUpperCase().indexOf(rfc) > -1 && td3.innerHTML.toUpperCase().indexOf(inst) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function buscarSolicitud(){
    var select, table;
    select = $('#select').val();
    table = document.getElementById("sinodales");
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
                if (td.innerHTML.toUpperCase() == "ACEPTADO") {
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
                if (td.innerHTML.toUpperCase() == "RECHAZADO") {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        } 
    }
}