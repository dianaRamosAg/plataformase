from .models import ArchivosAlumnos, ArchivosSinodales
from django import forms

class ArchivosAlumnosForm(forms.ModelForm):
    class Meta:
        model = ArchivosAlumnos
        fields = '__all__'

class ArchivosSinodalesForm(forms.ModelForm):
    class Meta:
        model = ArchivosSinodales
        fields = '__all__'