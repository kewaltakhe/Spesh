from django import forms
from .models import PhotoModel

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = PhotoModel
        fields = ('image','description')
        