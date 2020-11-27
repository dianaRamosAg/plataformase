function activarbBtnNS(){
    var selectcct = document.getElementById("select_cct");
    var btnNS = document.getElementById("btnNuevaSoli");
    if (selectcct.value != 'Seleccione el centro de trabajo'){
        btnNS.disabled=false;
    }
    else{
        btnNS.disabled=true;
    }
};


function creandoSoli(){
    var btnNS = document.getElementById("btnNuevaSoli");
    var divContainer = document.getElementById("buttonContainer");

    divContainer.innerHTML ="";
    //creamos el boton de cargando...
    var creandoBoton = document.createElement("button");
    creandoBoton.className="btn btn-primary mt-3";
    creandoBoton.innerHTML="Creando solicitud..."
    creandoBoton.disabled=true;

    //creamos el span para que gire
    var spanBoton = document.createElement("span");
    spanBoton.className="spinner-border spinner-border-sm";

    //agregamos el span al boton y el boton al div contenedor
    creandoBoton.appendChild(spanBoton);
    divContainer.appendChild(creandoBoton);

    //Depués de haber agregado el botón, enviamos el form para crear la solicitud

    document.getElementById("enviarSolicitud").submit();
    
};

function cargarListeners() { 
    var btnNS = document.getElementById("btnNuevaSoli");
    btnNS.addEventListener("click",creandoSoli,false);
    var selectcct = document.getElementById("select_cct");
    selectcct.addEventListener("change",activarbBtnNS,false);
};

function creandoSoli(){
    var btnNS = document.getElementById("btnNuevaSoli");
    var divContainer = document.getElementById("buttonContainer");

    divContainer.innerHTML ="";
    //creamos el boton de cargando...
    var creandoBoton = document.createElement("button");
    creandoBoton.className="btn btn-primary mt-3";
    creandoBoton.innerHTML="Creando solicitud..."
    creandoBoton.disabled=true;

    //creamos el span para que gire
    var spanBoton = document.createElement("span");
    spanBoton.className="spinner-border spinner-border-sm";

    //agregamos el span al boton y el boton al div contenedor
    creandoBoton.appendChild(spanBoton);
    divContainer.appendChild(creandoBoton);

    //Depués de haber agregado el botón, enviamos el form para crear la solicitud
    $("#enviarSolicitud").submit();
};

  document.addEventListener("DOMContentLoaded", cargarListeners, false);