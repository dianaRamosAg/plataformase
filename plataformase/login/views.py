# login/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from .forms import CustomUserCreationForm
from .models import CustomUser
from .forms import AcuerdosForms
from RVOES.models import Departamento, Acuerdos
from django.contrib.auth.hashers import make_password


"""
Todos los métodos (menos def perfil(request) ) incluyen el siguiente código:
#Si el tipo de usuario que hizo la solicitud es (4: administrador del sitio web)
if request.user.tipo_usuario == '4':
    #Código del método
    ....
#Si no corresponde el tipo de usuario lo manda a su página principal o login por defecto
else:
    return redirect('perfil')
"""

def SignUpView(request):
    """Esta vista permite a los administradores del sistema añadir nuevos usuarios.

    Parámetros
    -:param request: Contiene información del navegador del usuario esta realizando la petición.

    Retorna
    -:return render: Regresa la vista en la cual el usuario podrá añadir nuevos usuarios.
    """
    if request.user.tipo_usuario == '4':
        #Obtiene todos los departamentos registrados
        departamentos = Departamento.objects.all()
        idJefesDepReg = CustomUser.objects.values_list('departamento_id', flat=True).filter(jefe='1')
        return render(request, 'signup.html', {'departamentos': departamentos, 'jefes': list(idJefesDepReg) })
    else:
        return redirect('perfil')

def regUser(request):
    """Registra a los usuarios en la base de datos.

    Parámetros
    -:param request: Contiene información del navegador del usuario esta realizando la petición.

    Retorna
    -:return redirect 'root': Regresa a la pantalla principal del administrador del sistema.
    -:return redirect 'signup': Regresa la vista en la cual el usuario podrá añadir nuevos usuarios.
    """
    if request.user.tipo_usuario == '4':
        if request.method == 'POST':
            import datetime
            #Generamos las variables con los datos recibidos del request.
            username = request.POST["email"]
            curp_rfc = request.POST["curp_rfc"]
            calle = request.POST["calle"]
            password = make_password(request.POST["password2"])
            noexterior = request.POST["noexterior"]
            nointerior = request.POST["nointerior"]
            codigopostal = request.POST["codigopostal"]
            municipio = request.POST["municipio"]
            colonia = request.POST["colonia"]
            celular = request.POST["celular"]
            tipo_usuario = request.POST["tipo_usuario"]
            tipo_persona = request.POST["tipo_persona"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            if tipo_usuario!='2':
                firma_digital=request.POST["first_name"]
            else:
                firma_digital = request.FILES["firma_digital"]
            departamento = int(request.POST["departamento"])

    
            #Sí el usuario es jefe de departamento (tipo_usuario:2)
            if tipo_usuario == '2':
                #Definimos jefe como 1 (sí es jefe de departamento)
                jefe = '1'
            else:
                #Definimos jefe como 0 (no es jefe de departamento)
                jefe = '0'
                firma_digital= None
               
                #Si el tipo de usuario es institución(1) o administrador del sistema(4)
                if tipo_usuario == '1' or tipo_usuario == '4' or tipo_usuario=='5':
                    firma_digital= None
                    #Aseguramos que no pertenezcan a ningún departamento
                    departamento = None
            #Obtenemos el ID del usuario que registro a al nuevo usuario
            registro = (request.user.id)
            #Si existe un usuario que sea jefe de ese departamento
            if CustomUser.objects.filter(jefe='1', departamento_id=departamento).exists():
                #Se le hace usuario normal
                CustomUser.objects.filter(jefe='1', departamento_id=departamento).update(jefe='0')
            #Registramos el usuario en la base de datos
            usr = CustomUser(username=username, password=password, curp_rfc=curp_rfc, calle=calle,
                            noexterior=noexterior, nointerior=nointerior, codigopostal=codigopostal,
                            municipio=municipio, colonia=colonia, celular=celular, tipo_usuario=tipo_usuario,
                            tipo_persona=tipo_persona, first_name=first_name, last_name=last_name,
                            departamento_id=departamento, jefe=jefe, registro_id=registro,
                            date_joined=datetime.datetime.now(),firma_digital=firma_digital)
            usr.save()
            return redirect('usuarios')
        else:
            return redirect('signup')
    else:
        return redirect('perfil')

def docAnexos(request):
    """Registra acuerdos y visualiza los ya registrados.

    Parámetros
    -:param request: Contiene información del navegador del usuario esta realizando la petición.

    Retorna
    -:return: Regresa a la pantalla para que el usuario pueda añadir y ver los acuerdos.
    """
    if request.user.tipo_usuario == '4':
        #Inicializa la variable docs que almacena los acuerdos que se tienen registrados
        docs = None
        if request.method == 'POST':
            #Inicializamos una variable que contiene la información del formulario.
            form = AcuerdosForms(request.POST, request.FILES)
            #Si el formulario es válido.
            if form.is_valid():
                #Guardamos el formulario en la base de datos.
                form.save()
                return redirect('docAnexos')
        else:
            #Obtenemos el formulario predefinido de los acuerdos
            form = AcuerdosForms()
            #Obtenemos todos los acuerdos que ya se encuentran registrados
            docs = Acuerdos.objects.all()
        return render(request, 'root/docAnexos.html', {'form': form, 'docs': docs})
    else:
        return redirect('perfil')

def inicioRoot(request):
    """Redirige a la página de inicio del administrador del sistema.

    Parámetros
    -:param request: Contiene información del navegador del usuario esta realizando la petición.

    Retorna
    -:return: Redirige a la página de inicio del administrador del sistema.
    """
    if request.user.tipo_usuario == '4':
        return render(request, 'root/inicioRoot.html')
    else:
        return redirect('perfil')

def perfil(request):
    """Redirige a la página de inicio según el tipo de usuario.

    Parámetros
    -:param request: Contiene información del navegador del usuario esta realizando la petición.

    Retorna
    -:return: Redirige a la página de inicio según el tipo de usuario.
    """
    try:
        #Obtenemos el primer elemento de los departamentos.
        dep = Departamento.objects.get(id=1)
    except Departamento.DoesNotExist:
        #Si no existe un departamento, entonces los insertamos en la base de datos.
        a = Departamento(id=1, nombre='Control Escolar')
        a.save()
        b = Departamento(id=2, nombre='Dirección')
        b.save()
        c = Departamento(id=3, nombre='Superior')
        c.save()
        d = Departamento(id=4, nombre='Media Superior')
        d.save()
    #Si ya hay una sesión iniciada.
    if request.user.is_authenticated:
        #Si el tipo de usuario es institución (1)
        if request.user.tipo_usuario == '1':
            return redirect('menuinstitucion')
        #Si el tipo de usuario es jefe de departamento(2)   //rvoe  y examenes
        if request.user.departamento_id == 1:
            return redirect('control')
        if request.user.tipo_usuario == '2':
            return redirect('menudepartamento')
        #Si el tipo de usuario es subordinado de un jefe de departamento(3)
        if request.user.tipo_usuario == '3':
            return redirect('menudepartamento')
        #Si el tipo de usuario es administrador del sistema(4)  //registrar usuarios
        if request.user.tipo_usuario == '4':
            return redirect('menuadmin')
        #Usuario institución particular
        if request.user.tipo_usuario == '5':
            return redirect('menuparticular')
    else:#Si no hay sesión iniciada, le redirige al login
        return redirect('login')

def usuarios(request):
    """Esta vista permite a los administradores del sistema actualizar el estatus de los usuarios registrados.

    Parámetros
    -:param request: Contiene información del navegador del usuario esta realizando la petición.

    Retorna
    -:return render: Regresa la vista en la cual el usuario podrá actualizar el estatus de los usuarios.
    """
    usuarios = CustomUser.objects.all()
    return render(request, 'root/usuarios.html', {'usuarios': usuarios })


#----------------------------- VISITANTE ---------------------------------
#-------------------------------------------------------------------------
# '''Función que te redirige a la pantalla '''
# def visitante(request):
#     return render(request, 'signup_visitante.html')

# def Regvisitante(request):
#     if request.user.tipo_usuario == '4':
#         if request.method == 'get':
#             user = User.objects.get(username='uan@gmail.com')
#             user.set_password('123')
#             user.save()

#     return redirect('usuarios')


def editar(request,email):
    ''' Función editar, por medio del correo electronico se muestra 
    los permisos que pueden ser cambiados solo por el administrador.'''
    us = CustomUser.objects.get(username = email)
    return render(request,'editarpermisos.html',{'CustomUser':us})

def visit(request):
    '''Función que carga los departamentos a la ventana de solicitud de cuenta'''
    try:
        #Obtenemos el primer elemento de los departamentos.
        dep = Departamento.objects.get(id=1)
    except Departamento.DoesNotExist:
        #Si no existe un departamento, entonces los insertamos en la base de datos.
        a = Departamento(id=1, nombre='Control Escolar')
        a.save()
        b = Departamento(id=2, nombre='Dirección')
        b.save()
        c = Departamento(id=3, nombre='Superior')
        c.save()
        d = Departamento(id=4, nombre='Media Superior')
        d.save()
    if departamento=="Superior":
         return redirect('login')


'''Función para actualizar los permisos de los usuarios,por parte del administrador'''
def actualizarusr(request):
     if request.user.tipo_usuario == '4':
        if request.method == 'POST':
            email = request.POST["email"]
            tipo_usuario = request.POST["tipo_usuario"]
            departamento = int(request.POST["departamento"])
            if tipo_usuario=='3':
                 CustomUser.objects.filter(email=email).update(tipo_usuario=tipo_usuario,departamento_id=departamento)
                 return redirect('usuarios')
            if tipo_usuario=='2':
                CustomUser.objects.filter(email=email).update(tipo_usuario=tipo_usuario,departamento_id=departamento,jefe=1)
                return redirect('usuarios')

            if tipo_usuario=='4':
                CustomUser.objects.filter(email=email).update(tipo_usuario=tipo_usuario,departamento_id=None,jefe='0')
                return redirect('usuarios')

        else:
                return redirect('menuadmin')


def ActUsr(request,email):
    """ Actualizar/quitar departameto en caso de que se cambie a administrador
    """

    if request.user.tipo_usuario == '4':
        us = CustomUser.objects.get(username = email)
        #Obtiene todos los departamentos registrados
        departamentos = Departamento.objects.all()
        idJefesDepReg = CustomUser.objects.values_list('departamento_id', flat=True).filter(jefe='1')
        return render(request, 'editarpermisos.html', {'departamentos': departamentos, 'jefes': list(idJefesDepReg),'CustomUser':us })
    else:
        return redirect('perfil')
