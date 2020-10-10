from django import forms
from django.forms import ModelForm
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Client

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class MailForm(forms.Form):
    Subject = forms.CharField(label="Sujet", max_length=30, required=True)
    adresse_mail = forms.EmailField(required=True)
    Body = forms.CharField(label="Votre message", max_length=200, required=True, widget=forms.Textarea)


class ClientsForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class ResetPassword(forms.Form):
    adresse_mail = forms.CharField(label="adresse_mail", max_length=30, required=False)
    username = forms.CharField(label="username", max_length=30, required=False)


class ResetPasswordStep2(forms.Form):
    password = forms.PasswordInput()
    code = forms.CharField(label="username", max_length=30)

