# login/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from .forms import CustomUserCreationForm
from .models import CustomUser, UsuarioInstitucion
from .forms import AcuerdosForms
from RVOES.models import Departamento, Acuerdos
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


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
def SignUpViewtbc(request):
    # if request.user.tipo_usuario == '1':
    return render(request, 'signuptbc.html')

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
            if tipo_usuario=='1':
                inst_cct = request.POST["cct"]
                inst_nombredirector = request.POST["nombre_director"]
                sector = request.POST["sector"]
                nivel_educativo = request.POST["nivel_educativo"]
                if nivel_educativo=='1':
                    modalidad = request.POST["modalidad"]
                else:modalidad = "0"

            departamento = int(request.POST["departamento"])
            if tipo_usuario=='1' or tipo_usuario=='5': #Institución o Particular
                identificacion = request.POST["identificacion"]
                folio_id = request.POST["folio_id"]
                marca_educativa = request.POST["marca_educativa"]

                if tipo_persona == '2': # Tipo moral en Institución o Particular
                    nombre_representante = request.POST["nombre_representante"]
                    dom_legal_part = request.POST["dom_legal_part"]
                else:
                    nombre_representante = None
                    dom_legal_part = None
            else:
                identificacion = None
                folio_id = None
                marca_educativa = None
                nombre_representante = None
                dom_legal_part = None
                

            #Sí el usuario es jefe de departamento (tipo_usuario:2)
            if tipo_usuario == '2':
                #Definimos jefe como 1 (sí es jefe de departamento)
                jefe = '1'
            else:
                #Definimos jefe como 0 (no es jefe de departamento)
                jefe = '0'
                #No le asiganmos firma digital ya que no la necesita
                firma_digital= None
               
                #Si el tipo de usuario es institución(1) o administrador del sistema(4)
                if tipo_usuario == '1' or tipo_usuario == '4' or tipo_usuario =='5':
                    firma_digital= None
                    #Aseguramos que no pertenezcan a ningún departamento
                    departamento = None
            #Obtenemos el ID del usuario que registro a al nuevo usuario
            registro = (request.user.id)
            #Si existe un usuario que sea jefe de ese departamento
            if tipo_usuario == '2':
                if CustomUser.objects.filter(jefe='1', departamento_id=departamento).exists():
                #Se le hace usuario normal
                    CustomUser.objects.filter(jefe='1', departamento_id=departamento).update(jefe='0')
            #Registramos el usuario en la base de datos
            usr = CustomUser(username=username,email=username, password=password, curp_rfc=curp_rfc, calle=calle,
                            noexterior=noexterior, nointerior=nointerior, codigopostal=codigopostal,
                            municipio=municipio, colonia=colonia, celular=celular, tipo_usuario=tipo_usuario,
                            tipo_persona=tipo_persona, first_name=first_name, last_name=last_name,
                            departamento_id=departamento, jefe=jefe, registro_id=registro,
                            date_joined=datetime.datetime.now(), firma_digital=firma_digital, 
                            identificacion=identificacion,dom_legal_part=dom_legal_part,
                            folio_id=folio_id,nombre_representante=nombre_representante,
                            marca_educativa=marca_educativa)
            usr.save()
            if tipo_usuario == '1':
                usrInst = UsuarioInstitucion(id_usuariobase=usr, cct = inst_cct,
                                             nombredirector = inst_nombredirector, sector=sector,
                                             nivel_educativo=nivel_educativo,modalidad=modalidad)
                usrInst.save()
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
    if request.user.tipo_usuario == '2':
        #Inicializa la variable docs que almacena los acuerdos que se tienen registrados
        docs = None
        if request.method == 'POST':
            request.POST._mutable = True
            if request.POST['nivel'] == 'Superior':
                request.POST['nivel'] = '2'
            else:
                request.POST['nivel'] = '1'
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
            if request.user.departamento_id == 3:
                docs = Acuerdos.objects.filter(nivel='2')
            else:
                docs = Acuerdos.objects.filter(nivel='1')
        return render(request, 'root/docAnexos.html', {'form': form, 'docs': docs})
    else:
        return redirect('perfil')

def eliminarAcuerdo(request, id):
    Acuerdos.objects.filter(id=id).delete()
    return redirect('docAnexos')

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
            return redirect('menuinstitucion', request.user.id)
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
    usuarios = CustomUser.objects.filter(is_active=True)
    return render(request, 'root/usuarios.html', {'usuarios': usuarios })


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
            user = CustomUser.objects.get(email=email)
            if tipo_usuario=='3':
                 CustomUser.objects.filter(email=email).update(tipo_usuario=tipo_usuario,departamento_id=departamento)
                 return redirect('usuarios')
            if tipo_usuario=='2':
                if CustomUser.objects.filter(jefe='1', departamento_id=departamento).exists() :
                    #Se le hace usuario normal
                    CustomUser.objects.filter(jefe='1', departamento_id=departamento).update(jefe='0', tipo_usuario='3')
                    CustomUser.objects.filter(email=email).update(tipo_usuario=tipo_usuario,departamento_id=departamento,jefe=1)

                else:
                    CustomUser.objects.filter(email=email).update(tipo_usuario=tipo_usuario,departamento_id=departamento,jefe=1)
                if request.FILES:
                    if 'firma_digital' in request.FILES:
                        user.firma_digital.delete()
                        user.firma_digital = request.FILES['firma_digital']
                        user.tipo_usuario= tipo_usuario
                        user.departamento_id=departamento
                        user.jefe = 1
                user.save()
                return redirect('usuarios')
            if tipo_usuario=='4':
                CustomUser.objects.filter(email=email).update(tipo_usuario=tipo_usuario,departamento_id=None,jefe='0')
                return redirect('usuarios')

        else:
                return redirect('menuadmin')










def ActUsr(request,email):
    """ Actualizar/quitar departameto en caso de que se cambie a administrador
    """
    if CustomUser.objects.filter(email=email, tipo_usuario ='1').exists():
        return redirect('usuarios')
    if CustomUser.objects.filter(email=email, tipo_usuario ='5').exists():
        return redirect('usuarios')

    else:
        if request.user.tipo_usuario == '4':
            us = CustomUser.objects.get(username = email)
        #Obtiene todos los departamentos registrados
            departamentos = Departamento.objects.all()  
            idJefesDepReg = CustomUser.objects.values_list('departamento_id', flat=True).filter(jefe='1')
            return render(request, 'editarpermisos.html', {'departamentos': departamentos, 'jefes': list(idJefesDepReg),'CustomUser':us })
        else:
            return redirect('perfil')

  