from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': '用戶名稱'}))
    password = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={'placeholder': '密碼'}))

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': '用戶名稱'}))
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'placeholder': '電子郵件'}))
    password = forms.CharField(label='',
                               widget=forms.PasswordInput(attrs={'placeholder': '密碼'}))
    password2 = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={'placeholder': '密碼確認'}))
    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo',)
