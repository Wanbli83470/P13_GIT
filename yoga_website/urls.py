from django.contrib import admin

from django.urls import path

from yoga_website.views import (AtelierListView,
                                CreateAteliersView,
                                )

from. import views
urlpatterns = [
    path('', views.home, name="home"),
    path('yoga', views.yoga, name="yoga"),
    path('video', views.video, name="video"),
    path('connexion', views.connexion, name="connexion"),
    path('deconnexion', views.deconnexion, name="deconnexion"),
    path('inscription', views.register, name="inscription"),
    path('ateliers', views.ateliers, name="ateliers"),
    path('detailAteliers/<int:idatelier>/<int:idclient>', views.detailAteliers, name="detailAteliers"),
    path('contact', views.contact, name="contact"),
    path('register', views.register, name="register"),
    path('espace', views.espace, name="espace"),
    path('clients', views.clients, name="clients"),
    path('nidra', views.nidra, name="nidra"),
    path('participants/<int:idAtelier>', views.participants, name="participants"),
    path('test', AtelierListView.as_view(), name="test"),
    path('inscribe/<int:idatelier>/<int:idclient>', views.inscribe, name="inscribe"),
    path('unsubscribe/<int:idatelier>/<int:idclient>', views.unsubscribe, name="unsubscribe"),
    path('new-atelier/', CreateAteliersView.as_view(), name="create-atelier"),
    path('registrationValid/<str:username>/<str:email>', views.registrationValid, name="registrationValid"),
    path('deleteAtelier/<int:idAtelier>', views.deleteAtelier, name="deleteAtelier"),
    path('delete_compte', views.delete_compte, name="delete_compte"),
    path('resetPassword', views.resetPassword, name="reset_password"),
    path('resetPasswordStep/<str:username>/<str:adresse_mail>', views.resetPasswordStep, name="resset_password_step"),
]
