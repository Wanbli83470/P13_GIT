from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from .forms import ConnexionForm, MailForm, RegistrationForm, ClientsForm
from .citation import phrase_du_jour
from django.core.mail import EmailMessage
from django.urls import reverse
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DeleteView
    )
from yoga_website.models import Atelier, Client, Inscribe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .generate_pdf import form_adhesion
import time
from django.urls import reverse
import os

var_color = "vert"
admin = False
mail_soph = os.environ.get("ADRESS_P13_MAIL")
def get_id_client(request):
    username = request.user
    client = Client.objects.get(user=username)
    return client.id

def user_actif(request):
    list_client = []
    for c in Client.objects.all():
        print(c.user)
        list_client.append(str(c.user))

    print(list_client)
    global var_color
    global admin
    print("utilisateur connecté : {}".format(request.user))
    mon_user = str(request.user)
    print(mon_user)
    user = str
    print(var_color)
    if mon_user == "admin":
        print("admin connecté")
        var_color = "violet"
        admin = True
        user1 = "admin"
        print(var_color, admin)
    elif mon_user in list_client :
        var_color = "vert"
        user1 = "client"
        print(">>> Client enregistré et validé : {}".format(mon_user))
        admin = False
    elif mon_user not in list_client and mon_user is not "AnonymousUser" :
        user1 = "client_not_active"
        var_color = "vert"
    elif mon_user == "AnonymousUser":
        var_color = "vert"
        user1 = "new_user"
    return user1
    print(user1)

def home(request):
    user1 = user_actif(request)
    print(user1)
    return render(request, "yoga_website/bienvenu.html", {'phrase_du_jour': phrase_du_jour, 'var_color':var_color, 'admin':admin, 'user1':user1})

def yoga(request):
    user1 = user_actif(request)
    return render(request, "yoga_website/yoga.html", {'var_color':var_color, 'var_color':var_color, 'admin':admin, 'user1':user1})


def nidra(request):
    user1 = user_actif(request)
    return render(request, "yoga_website/nidra.html", {'video':video, 'var_color':var_color, 'user1':user1})

def video(request):
    user1 = user_actif(request)
    video = True
    return render(request, "yoga_website/vidéo.html", {'video':video, 'var_color':var_color, 'admin':admin, 'user1':user1})

def espace(request):
    user1 = user_actif(request)
    return render(request, "yoga_website/espace.html", {'var_color':var_color, 'var_color':var_color, 'admin':admin, 'user1':user1})

def registrationValid(request, username, email):
    user1 = user_actif(request)
    Subject = "Votre inscription sur melodyoga"
    adresse_mail = mail_soph
    Body = f"Bonjour {username} Nous vous confirmons votre inscription sur melodyoga, En vous souhaitant une bonne journée"
    email_confirm = EmailMessage(Subject, Body, adresse_mail, [email])
    email_confirm.content_subtype = "html"
    email_confirm.attach_file('Forumulaire_adhésion.pdf')
    email_confirm.send()

    email_confirm_me = EmailMessage(Subject, Body, adresse_mail, [adresse_mail])
    email_confirm.content_subtype = "html"
    email_confirm_me.attach_file('Forumulaire_adhésion.pdf')
    email_confirm_me.send()
    print("mail envoyé")
    username = str(username)
    return render(request, 'yoga_website/registration_valid.html', {'username': username, 'email': email, 'var_color':var_color, 'admin':admin, 'user1':user1})

def register(request):
    user1 = user_actif(request)
    error = False
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("ok compte (:")
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            messages.success(request, f'Votre compte {username} est crée')
            form_adhesion(email=email, username=username)
            return redirect("registrationValid", username=username, email=email)
        else :
            error = True
            print(error)
            print("Echec")
    else :
        form = RegistrationForm(request.POST)

    return render(request, 'yoga_website/register.html', {'form':form, 'var_color':var_color, 'admin':admin, 'user1':user1})

def connexion(request):
    user1 = user_actif(request)
    error = False
    print("vue connexion")
    if request.method == "POST":
        print("Méthode POST ok")
        form = ConnexionForm(request.POST or None)
        if form.is_valid():
            print("form valide !")
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                print("redirection accueil")
                return redirect('/')
            else: # sinon une erreur sera affichée
                print("Else !")
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'yoga_website/connect.html', {'form':form,'error':error, 'var_color':var_color, 'admin':admin, 'user1':user1})

def contact(request):
    user1 = user_actif(request)
    print("vue mail")
    form_class = MailForm
    mail_form = form_class(request.POST or None)

    if request.method == "POST":
        print("Méthode POST ok")

        if mail_form.is_valid():
            print("form MAIL valide")
            Subject = mail_form.cleaned_data["Subject"]
            adresse_mail = mail_form.cleaned_data["adresse_mail"]
            Body = mail_form.cleaned_data["Body"] + " " + adresse_mail
            email = EmailMessage("Melodyoga : " + Subject, Body, mail_soph, [mail_soph])
            print(Subject, Body)
            print(email)

            email.send()
            print("mail envoyé")
            return redirect('/home')

    return render(request, 'yoga_website/contact.html', {'mail_form':mail_form, 'var_color':var_color, 'admin':admin, 'user1':user1})

def deconnexion(request):
    user1 = user_actif(request)
    global var_color
    global admin
    logout(request)
    var_color = "vert"
    admin = False
    print("var_color devient {}".format(var_color))
    return redirect('home')

class AtelierListView(ListView):
    model = Atelier
    template_name = 'yoga_website/ateliers.html'
    context_object_name = "ateliers"

class CreateAteliersView(LoginRequiredMixin, CreateView):
    model = Atelier
    fields = ['type', 'nb_places', 'date', 'lieux', 'places']
    template_name = 'yoga_website/atelier_form.html'


def ateliers(request):
    id_client = get_id_client(request)
    user1 = user_actif(request)
    ateliers = Atelier.objects.order_by('date')

    return render(request, 'yoga_website/ateliers.html', {'ateliers': ateliers, 'var_color': var_color, 'admin': admin, 'user1': user1, 'id_client': id_client})

def detailAteliers(request, idatelier, idclient):
    user1 = user_actif(request)
    idatelier = idatelier
    idclient = idclient

    atelier = Atelier.objects.get(id=idatelier)
    print(atelier)
    client = Client.objects.get(id=idclient)
    print(client)
    nb_participants = Inscribe.objects.filter(atelier=atelier)
    nb_participants = len(nb_participants)
    places_restantes = atelier.nb_places - nb_participants
    Places = True
    if places_restantes == 0 :
        Places = False
    else :
        Places = True
    go_inscribe = True
    try:
        go = Inscribe.objects.get(client=client, atelier=atelier)
        go_inscribe = False
    except Inscribe.DoesNotExist:
        go = None
        go_inscribe = True
    return render(request, 'yoga_website/detailAtelier.html',
                  {'var_color': var_color, 'admin': admin, 'user1': user1,
                   'go_inscribe': go_inscribe, 'atelier':atelier, 'idatelier': idatelier, 'idclient':idclient, 'nb_participants':nb_participants, 'places_restantes':places_restantes, 'Places':Places})

def participants(request, idAtelier):
    user1 = user_actif(request)
    if user1 != "admin":
        return redirect ('home')
    idAtelier = idAtelier
    select_atelier = Atelier.objects.get(id=idAtelier)
    select_participants = Inscribe.objects.filter(atelier=select_atelier)
    nb_participants = len(select_participants)
    places_restantes = select_atelier.nb_places - nb_participants
    print(select_atelier)
    print(select_participants)
    return render(request, 'yoga_website/participants.html', {'var_color': var_color, 'admin': admin, 'user1': user1, 'idAtelier': idAtelier, "select_participants":select_participants, "select_atelier":select_atelier, 'places_restantes':places_restantes})

def deleteAtelier(request, idAtelier):
    user1 = user_actif(request)
    idAtelier = idAtelier
    selectAtelier = Atelier(id=idAtelier)
    selectAtelier.delete()
    return render(request, 'yoga_website/ateliers.html', {'var_color':var_color, 'admin':admin, 'user1':user1})

def clients(request):
    user1 = user_actif(request)
    Clients = Client.objects.all()
    if request.method == "POST":
        form = ClientsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients')
        else :
            error = True
            print(error)
            print("Echec")
    else :
        form = ClientsForm(request.POST)

    return render(request, 'yoga_website/clients.html', {"Clients": Clients, "form":form, 'var_color':var_color, 'admin':admin, 'user1':user1})

def inscribe(request, idatelier, idclient):
    user1 = user_actif(request)
    idatelier = idatelier
    idclient = idclient

    username = str(request.user)
    email = Client.objects.get(id=idclient)
    email = email.email
    print(email)



    atelier = Atelier.objects.get(id=idatelier)
    print(atelier)
    client = Client.objects.get(id=idclient)
    print(client)
    save = Inscribe(client=client, atelier=atelier)
    save.save()

    Subject = f"{username} Votre inscription : Atelier chez Melodyoga"
    adresse_mail = mail_soph
    Body = f"Bonjour {username} Nous vous confirmons votre inscription pour l'atelier en date du {atelier.date}, en vous souhaitant une bonne journée."
    email_confirm = EmailMessage(Subject, Body, adresse_mail, [email])
    email_confirm.send()

    email_confirm_me = EmailMessage(Subject, Body, adresse_mail, [adresse_mail])
    email_confirm_me.send()
    return render(request, 'yoga_website/inscribe.html', {'var_color': var_color, 'admin': admin, 'user1': user1})

def unsubscribe(request, idatelier, idclient):
    user1 = user_actif(request)
    idatelier = idatelier
    idclient = idclient

    atelier = Atelier.objects.get(id=idatelier)
    print(atelier)
    client = Client.objects.get(id=idclient)
    print(client)
    del_ = Inscribe.objects.get(client=client, atelier=atelier)
    del_.delete()

    username = str(request.user)
    email = Client.objects.get(id=idclient)
    email = email.email
    print(email)

    Subject = "Votre déinscription : Atelier chez Melodyoga"
    adresse_mail = mail_soph
    Body = f"Bonjour {username} Nous avons bien noté votre annulation pour l'atelier en date du {atelier.date} et espérons vous revoir prochainement."
    email_confirm = EmailMessage(Subject, Body, adresse_mail, [email])
    email_confirm.send()

    email_confirm_me = EmailMessage(Subject, Body, adresse_mail, [adresse_mail])
    email_confirm_me.send()


    return render(request, 'yoga_website/unsubscribe.html', {'var_color': var_color, 'admin': admin, 'user1': user1})

    return redirect('home')