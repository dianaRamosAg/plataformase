
from django.core.exceptions import ValidationError

def valid_extension(value):
    """Valida que la extención del documento sea PDF"""
    if not value.name.endswith('.pdf'):#Si la extención no es PDF
        raise ValidationError("Solo puede subir archivos con extención \".pdf\"")#Retorna mensaje de error