from django import forms
from .models import Institucion
class ImagenesInstitucion(forms.ModelForm):
    class Meta:
        model = Institucion
        fields = ('ImagenNo1','ImagenNo2','ImagenNo3')