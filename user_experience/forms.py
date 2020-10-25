from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Client
from django.core.exceptions import ValidationError


class RegistrationForm(UserCreationForm):
    """Account creation form"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
        return self.cleaned_data


class ConnectionForm(forms.Form):
    """Login form"""
    username = forms.CharField(label="Nom d'utilisateur ou adresse email", max_length=40)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class MailForm(forms.Form):
    """Mail form"""
    Subject = forms.CharField(label="Sujet", max_length=30, required=True)
    mail_adress = forms.EmailField(required=True)
    Body = forms.CharField(label="Votre message", max_length=300,
                           required=True, widget=forms.Textarea)


class ResetPassword(forms.Form):
    """Form to obtain the user ID"""
    mail_adress = forms.EmailField(label="adresse_mail", max_length=30, required=False)
    username = forms.CharField(label="username", max_length=20, required=False)


class ResetPasswordStep2(forms.Form):
    """New Password Form"""
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    code = forms.CharField(label="Code Email", max_length=5)


class ClientModif(forms.Form):
    """User details modification form"""
    username = forms.CharField(label="Nom d'utilisateur", max_length=20)
    email_adress = forms.EmailField(label="Mon adresse email", max_length=50)
    phone = forms.CharField(label="N°tél :", max_length=10, min_length=10)

    def clean(self):
        email_adress = self.cleaned_data.get('email_adress')
        phone = self.cleaned_data.get('phone')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email_adress).exists():
            raise ValidationError("Email exists")
        if Client.objects.filter(Phone=phone).exists():
            raise ValidationError("phone exists")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Nom d'utilisateur existant")
        return self.cleaned_data


class UserModif(forms.Form):
    """User details modification form"""
    username = forms.CharField(label="Nom d'utilisateur", max_length=20)
    email_adress = forms.EmailField(label="Mon adresse email", max_length=50)

    def clean(self):
        email_adress = self.cleaned_data.get('email_adress')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email_adress).exists():
            raise ValidationError("Email exists")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Nom d'utilisateur existant")
        return self.cleaned_data


class UploadFileForm(forms.Form):
    pdf_file = forms.FileField(label="Ma demande (Format PDF)")

    def clean(self):
        name_file = self.cleaned_data.get('pdf_file')
        if "pdf" in name_file:
            print("pdf okay")
            raise ValidationError("Ceci n'est pas un fichier pdf")
        return self.cleaned_data
