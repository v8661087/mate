from django import forms
from .models import Image, Comment


class ImageCreateForm(forms.ModelForm):


    class Meta:
        model = Image
        fields = ('title',  'image', 'description',)


class CommentForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': '留言‧‧‧‧‧'}))


    class Meta:
        model = Comment
        fields = ('body', )

