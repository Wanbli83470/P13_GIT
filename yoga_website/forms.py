from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Client


class RegistrationForm(UserCreationForm):
    """Account creation form"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )


class ConnexionForm(forms.Form):
    """Login form"""
    username = forms.CharField(label="Nom d'utilisateur", max_length=20)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class MailForm(forms.Form):
    """Mail form"""
    Subject = forms.CharField(label="Sujet", max_length=30, required=True)
    adresse_mail = forms.EmailField(required=True)
    Body = forms.CharField(label="Votre message", max_length=200,
                           required=True, widget=forms.Textarea)


class ClientsForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class ResetPassword(forms.Form):
    """Form to obtain the user ID"""
    adresse_mail = forms.CharField(label="adresse_mail", max_length=30, required=False)
    username = forms.CharField(label="username", max_length=20, required=False)


class ResetPasswordStep2(forms.Form):
    """New Password Form"""
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    code = forms.CharField(label="Code Email", max_length=30)


class UserModif(forms.Form):
    """User details modification form"""
    username = forms.CharField(label="username", max_length=20)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    adresse_mail = forms.EmailField(label="Email")
    tel = forms.CharField(label="N°Tél", max_length=10)


class UploadFileForm(forms.Form):
    pdf_file = forms.FileField(label="Ma demande (Format PDF)")
