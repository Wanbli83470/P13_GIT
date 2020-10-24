from django import forms
from django.forms import ModelForm
from user_experience.models import Client


class ConnectionForm(forms.Form):
    """Login form"""
    username = forms.CharField(label="Nom d'utilisateur ou adresse email", max_length=40)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class ClientsForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
