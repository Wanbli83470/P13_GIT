from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import random
# Create your models here.


class PdfInput(models.Model):
    """SQL table associating the membership form with the user"""
    user = models.OneToOneField(User, on_delete=ChildProcessError)
    pdf_file = models.FileField(upload_to='yoga_website/static/yoga_website/')


class PdfOutput(models.Model):
    """SQL table associating the membership form with the user"""
    user = models.OneToOneField(User, on_delete=ChildProcessError)
    pdf_file = models.FileField(upload_to='yoga_website/static/yoga_website/pdf_output/')


class Atelier(models.Model):
    """SQL table containing information for each workshop"""
    type = models.CharField(max_length=30)
    nb_places = models.IntegerField()
    places = models.BooleanField(default=True)
    date = models.DateTimeField()
    lieux = models.CharField(max_length=50)

    def __str__(self):
        """Customizing the print python method"""
        return "ATELIER : {} ||| DATE : {} ||| PLACES : {} ||| ID : {} "\
            .format(self.type, self.date, self.nb_places, self.id)

    def get_absolute_url(self):
        return reverse('ateliers')


class Client(models.Model):
    """SQL table containing the information of each client of the association"""
    user = models.OneToOneField(User, on_delete=ChildProcessError)
    prenom = models.CharField(max_length=254, default="test")
    nom = models.CharField(max_length=255)
    tel = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return "CLIENT : {} NOM : {} ID : {}\n Tél : {} Email : {}"\
            .format(self.prenom, self.nom, self.id, self.tel, self.email)


class Inscribe(models.Model):
    """SQL table managing customer registration for workshops"""
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    atelier = models.ForeignKey(Atelier, on_delete=models.CASCADE)

    def __str__(self):
        return "id = " + str(self.atelier.id)


class SecretCode(models.Model):
    """SQL table containing the secret code for each user"""
    user = models.OneToOneField(User, on_delete=ChildProcessError)
    code = models.CharField(max_length=254, default=str(random.randint(10000, 100000)))

    def __str__(self):
        return f"Utilisateur : {self.user.username} / Code secret : {self.code}"
