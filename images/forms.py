from django import forms
from .models import Image
from PIL import Image as Image2
from django.core.files import File

class ImageCreateForm(forms.ModelForm):


    class Meta:
        model = Image
        fields = ('title',  'image', 'description',)




