from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': '用戶名稱'}))
    password = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={'placeholder': '密碼'}))

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': '用戶名稱'}))
    email = forms.EmailField(label='', required=False, widget=forms.EmailInput(attrs={'placeholder': '電子郵件'}))
    password = forms.CharField(min_length=8, label='',
                               widget=forms.PasswordInput(attrs={'placeholder': '密碼'}))
  #  password2 = forms.CharField(label='',
   #                             widget=forms.PasswordInput(attrs={'placeholder': '密碼確認'}))
    class Meta:
        model = User
        fields = ('email', 'username', 'password')

  #  def clean_password2(self):
   #     cd = self.cleaned_data
   #     if cd['password'] != cd['password2']:
  #          raise forms.ValidationError('Passwords don\'t match.')
   #     return cd['password2']


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('photo',)
        widgets = {
            'photo': forms.HiddenInput,
        }

class UserEditForm(forms.ModelForm):
    username = forms.CharField(label='用戶名稱')

    class Meta:
        model = User
        fields = ('username', 'email',)


class OtherProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('full_name', 'website', 'personal_profile', 'phone_number', 'gender' )


class FullnameForm(forms.ModelForm):
    full_name = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': '全名'}))

    class Meta:
        model = Profile
        fields = ('full_name', )


