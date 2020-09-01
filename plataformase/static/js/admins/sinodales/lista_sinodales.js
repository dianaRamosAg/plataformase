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
    ba.style.display='none'
    var table, inst, name, rfc;
    name = $('#nombre').val().toUpperCase();
    inst = $('#institucion').val().toUpperCase();
    rfc = $('#rfc').val().toUpperCase();
    table = document.getElementById("sinodales");
    tr = table.getElementsByTagName("tr");

    for(i=1;i<tr.length;i++) {
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
}

function buscarsino() {
    var table, inst, name, rfc;
    name = $('#nombre').val().toUpperCase();
    inst = $('#institucion').val().toUpperCase();
    rfc = $('#rfc').val().toUpperCase();
    table = document.getElementById("sinodales");
    tr = table.getElementsByTagName("tr");

    for(i=1;i<tr.length;i++) {
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

