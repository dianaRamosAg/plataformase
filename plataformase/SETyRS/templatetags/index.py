from django import template
register = template.Library()

# Estas funciones son para la etiqueta index en el html utilizada para organizar los documentos en la tabla y poder visualizarlos
# La manera en que se utiliza es:
# {% index DICCIONARIO_CON_LOS_ARCHIVOS ID_DEL_ALUMNO %} para los archivos de los alumnos enlistados
# y
# {% index DICCIONARIO_CON_LOS_ARCHIVOS ID_DEL_SINODAL %} para los archivos de los sinodales enlistados
# Esto retorna un diccionario con los archivos del alumno o del sinodal correspondiente al ciclo de la lista a la hora de crear las filas de la tabla

@register.simple_tag
def index(indexable, id):
    lista = []
    for i in indexable:
        lista.append(i.alumno_id)
    if id in lista:
        return True
    else:
        return False

@register.simple_tag
def indexS(indexable, id):
    lista = []
    for i in indexable:
        lista.append(i.sinodal_id)
    if id in lista:
        return True
    else:
        return False

@register.simple_tag
def doc(indexable, id):
    docs = {}
    for a in indexable:
        if a.alumno_id == id:
            docs['id']=a.alumno_id
            docs['certi']=a.certificado_egreso
            docs['cotejo']=a.servicio_social
            docs['control']=a.inscripcion_ctrl_escolar
            docs['recibo']=a.recibo_pago
    return docs

@register.simple_tag
def docS(indexable, id):
    docs = {}
    for a in indexable:
        if a.sinodal_id == id:
            docs['id']=a.sinodal_id
            docs['curr']=a.curriculum
            docs['ced']=a.cedula
    return docs