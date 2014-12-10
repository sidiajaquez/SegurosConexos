#encoding:utf-8
from django import forms

from .models import ImagenSiniestro

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = ImagenSiniestro
        exclude = ['Thumbnail']