from .models import Solicitud, Notificacion, CInstitucional, CCurricular, CAcademica, CMedSuperior, Comentarios
from django import forms

class SolicitudForms(forms.ModelForm):

    class Meta:
        model = Solicitud
        fields = ('nivel', 'modalidad', 'salud', 'customuser', 'estatus',
                  'noInstrumentoNotarial', 'nombreNotario', 'noNotario',
                  'nombreRepresentante', 'nombreSolicitud')

class ComentariosForms(forms.ModelForm):

    class Meta:
        model = Comentarios
        fields = ('descripcion',)

class ArchivosMedSupForm(forms.ModelForm):
    class Meta:
        model = CMedSuperior
        fields = '__all__'

class ArchivosInstForm(forms.ModelForm):
    class Meta:
        model = CInstitucional
        fields = '__all__'


class ArchivosCCurrForm(forms.ModelForm):
    class Meta:
        model = CCurricular
        fields = ('id_solicitud', 'estudio', 'plan', 'mapa', 'programa',
            'metodologia', 'cifrhs', 'carta')

class ArchivosCAcadForm(forms.ModelForm):
    class Meta:
        model = CAcademica
        fields = ('id_solicitud', 'rec_bibliograficos', 'rec_didacticos',
            'talleres', 'apoyo_informatico', 'apoyo_comunicaciones',
            'personal')
