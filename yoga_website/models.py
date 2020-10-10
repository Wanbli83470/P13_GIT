from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Pdf(models.Model):
    user = models.OneToOneField(User, on_delete=ChildProcessError)
    chemin_file_pdf = models.CharField(max_length=50)


class Atelier(models.Model):
    type = models.CharField(max_length=30)
    nb_places = models.IntegerField()
    places = models.BooleanField(default=True)
    date = models.DateTimeField()
    lieux = models.CharField(max_length=50)

    def __str__(self):
        return "ATELIER : {} ||| DATE : {} ||| PLACES : {} ||| ID : {} ".format(self.type, self.date, self.nb_places, self.id)

    def get_absolute_url(self):
        return reverse('ateliers')


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=ChildProcessError)
    prenom = models.CharField(max_length=254, default="test")
    nom = models.CharField(max_length=255)
    tel = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return "CLIENT : {} NOM : {} ID : {}\n Tél : {} Email : {}".format(self.prenom, self.nom, self.id, self.tel, self.email)


class Inscribe(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    atelier = models.ForeignKey(Atelier, on_delete=models.CASCADE)

    def __str__(self):
        return "INSCRIPTION DE : \n {} POUR ATELIER : {}".format(self.client, self.atelier)
