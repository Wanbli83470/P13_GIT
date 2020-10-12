from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from .forms import ConnexionForm, MailForm, RegistrationForm, ClientsForm, ResetPassword, ResetPasswordStep2
from .citation import phrase_du_jour
from django.core.mail import EmailMessage
from django.urls import reverse
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DeleteView
    )
from yoga_website.models import Atelier, Client, Inscribe, Pdf, SecretCode
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
import random

var_color = "vert"
admin = False
mail_soph = os.environ.get("ADRESS_P13_MAIL")

def user_actif(request):
    list_client = []
    for c in Client.objects.all():
        print(c.user)
        list_client.append(str(c.user))

    print(list_client)
    global var_color
    global admin
    mon_user = str(request.user)
    user = str
    if mon_user == "thomas":
        print("admin connecté")
        var_color = "violet"
        admin = True
        user1 = "admin"
    elif mon_user in list_client:
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


def get_id_client(request):
    username = request.user
    client = Client.objects.get(user=username)
    return client.id


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
    user = request.user
    pdf_user = Pdf.objects.get_or_create(user=user, chemin_file_pdf="dawa.pdf")
    client = Client.objects.get(user=user)
    sessions = Inscribe.objects.filter(client=client)
    nb_sessions = len(sessions)
    user1 = user_actif(request)
    #chemin_pdf = "/static/adhésion/Forumulaire_adhésion_Franck899.pdf"
    chemin_pdf = f"/static/adhésion/Forumulaire_adhésion_{request.user}.pdf"
    return render(request, "yoga_website/espace.html", {'var_color': var_color, 'admin': admin,
                                                        'user1': user1, 'chemin_pdf': chemin_pdf,
                                                        'nb_sessions': nb_sessions, 'client': client})


def registrationValid(request, username, email):

    user1 = user_actif(request)
    Subject = "Votre inscription sur melodyoga"
    adresse_mail = mail_soph
    Body = f"Bonjour {username} Nous vous confirmons votre inscription sur melodyoga, En vous souhaitant une bonne journée"
    email_confirm = EmailMessage(Subject, Body, adresse_mail, [email])
    email_confirm.content_subtype = "html"
    email_confirm.attach_file(f"yoga_website/formulaire_adhésion_{username}.pdf")
    email_confirm.send()

    email_confirm_me = EmailMessage(Subject, Body, adresse_mail, [adresse_mail])
    email_confirm.content_subtype = "html"
    email_confirm_me.attach_file(f"yoga_website/formulaire_adhésion_{username}.pdf")
    email_confirm_me.send()
    print("mail envoyé")
    username = str(username)
    print("request.user : ")
    print(request.user)
    return render(request, 'yoga_website/registration_valid.html', {'username': username, 'email': email, 'var_color': var_color,
                                                                    'admin': admin, 'user1': user1})


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
        else:
            error = True
            print(error)
            print("Echec")
    else:
        form = RegistrationForm(request.POST)

    return render(request, 'yoga_website/register.html', {'form': form, 'var_color': var_color, 'admin': admin, 'user1': user1})


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

    return render(request, 'yoga_website/connect.html', {'form': form,'error': error, 'var_color': var_color,
                                                         'admin': admin, 'user1': user1})


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
    user1 = user_actif(request)
    ateliers = Atelier.objects.order_by('date')
    if user1 != "admin":
        id_client = get_id_client(request)
    else:
        id_client = 0
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
    if places_restantes == 0:
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
    return render(request, 'yoga_website/participants.html', {'var_color': var_color, 'admin': admin, 'user1': user1, 'idAtelier': idAtelier, "select_participants": select_participants, "select_atelier": select_atelier, 'places_restantes': places_restantes, 'nb_participants': nb_participants})


def deleteAtelier(request, idAtelier):
    user1 = user_actif(request)
    idAtelier = idAtelier
    selectAtelier = Atelier(id=idAtelier)
    selectAtelier.delete()
    return render(request, 'yoga_website/ateliers.html', {'var_color': var_color, 'admin': admin, 'user1': user1})


def clients(request):
    user1 = user_actif(request)
    Clients = Client.objects.all()
    if request.method == "POST":
        form = ClientsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients')
        else:
            error = True
            print(error)
            print("Echec")
    else:
        form = ClientsForm(request.POST)

    return render(request, 'yoga_website/clients.html', {"Clients": Clients, "form": form, 'var_color': var_color,
                                                         'admin': admin, 'user1': user1})


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


def delete_compte(request):
    user = request.user
    user1 = user_actif(request)

    try:
        secretCode = SecretCode.objects.get(user=user)
        secretCode.delete()
    except :
        pass

    if user1 == "client":
        compte_delete = Client.objects.get(user=user)
        print("Client actif")
        for i in Inscribe.objects.filter(client=compte_delete):
            print(i.client)
            i.delete()



        pdf_delete = Pdf.objects.get(user=user)
        pdf_delete.delete()
        compte_delete.delete()
        user.delete()

    else:
        print("Client not active")
        pdf_delete = Pdf.objects.get(user=user)
        pdf_delete.delete()
        user.delete()

    """Mail de confirmation"""
    Subject = "Suppresion de votre compte sur melodyoga"
    adresse_mail = mail_soph
    Body = f"Bonjour {user.username} Nous vous confirmons suppresion de votre compte sur melodyoga, En vous souhaitant une bonne journée"
    email_confirm = EmailMessage(Subject, Body, adresse_mail, [user.email])
    email_confirm.send()

    email_confirm_me = EmailMessage(Subject, Body, adresse_mail, [adresse_mail])
    email_confirm_me.send()

    return redirect('home')


def resetPassword(request):

    if request.method == "POST":
        print("Méthode POST ok")
        form_password = ResetPassword(request.POST)

        if form_password.is_valid():
            print("form password valide")
            username = form_password.cleaned_data["username"]
            adresse_mail = form_password.cleaned_data["adresse_mail"]
            if username == "":
                username = "null"
            if adresse_mail == "":
                adresse_mail = "null"
            print(username, adresse_mail)
            return redirect("resset_password_step", username=username, adresse_mail=adresse_mail,)
        else:
            error = True
            print(error)
            print("Echec")
    else:
        form_password = ResetPassword()

    return render(request, 'yoga_website/reset_password.html', {'var_color': var_color, 'admin': admin,
                                                                'form_password': form_password})


def resetPasswordStep(request, username, adresse_mail):
    username, adresse_mail = username, adresse_mail
    utilisateur, echec = None, False

    """On détermine l'utilisateur"""
    if username == "null" and adresse_mail == "null":
        echec = True
    else:
        try:
            utilisateur = User.objects.get(email=adresse_mail)
            secret_entrance = SecretCode.objects.get_or_create(user=utilisateur)
            secret_entrance = SecretCode.objects.get(user=utilisateur)
            """Mail contenant le code secret"""
            Subject = "Demande changement du mot de passe sur melodyoga"
            adresse_mail = mail_soph
            Body = f"Bonjour {utilisateur.username} Voici votre code secret {secret_entrance.code} " \
                   f"Celui-ci vous sera demandé à l'étape suivante pour modifier votre mot de passe"
            email_confirm = EmailMessage(Subject, Body, adresse_mail, [utilisateur.email])
            email_confirm.send()
            username = utilisateur.username
        except:
            try:
                utilisateur = User.objects.get(username=username)
                secret_entrance = SecretCode.objects.get_or_create(user=utilisateur)
                secret_entrance = SecretCode.objects.get(user=utilisateur)
                """Mail contenant le code secret"""
                Subject = "Demande changement du mot de passe sur melodyoga"
                adresse_mail = mail_soph
                Body = f"Bonjour {utilisateur.username} Voici votre code secret {secret_entrance.code} " \
                       f"Celui-ci vous sera demandé à l'étape suivante pour modifier votre mot de passe"
                email_confirm = EmailMessage(Subject, Body, adresse_mail, [utilisateur.email])
                email_confirm.send()

            except:
                echec = True

    print(echec)

    if request.method == "POST":
        print("Méthode POST ok")
        form_password = ResetPasswordStep2(request.POST)

        if form_password.is_valid():
            print("form password valide")
            code = form_password.cleaned_data["code"]
            password = str(form_password.cleaned_data["password"])
            print(code, str(secret_entrance.code))

            if str(code) == str(secret_entrance.code):
                print("Changement du password autorisé ! ")
                utilisateur.set_password(password)
                utilisateur.save()
                print(utilisateur)
                print(utilisateur.password)
                """On attribue un nouveau code secret pour l'avenir"""
                code_secret = str(random.randint(10000, 100000))
                print("code généré : " + code_secret)
                secret_entrance = SecretCode.objects.get(user=utilisateur)
                secret_entrance.code = str(code_secret)
                secret_entrance.save()

                """Confirmation changement de mot de passe"""
                Subject = "Mot de passe modifié Melodyoga"
                adresse_mail = mail_soph
                Body = f"{utilisateur.username} Nous vous confirmons le changement de mot de passe " \
                       f"suite à votre procédure sur notre site"
                email_confirm = EmailMessage(Subject, Body, adresse_mail, [utilisateur.email])
                email_confirm.send()

                """Redirection"""
                return redirect("home")

            else:
                print("Changement de passward non autorisé")

        else:
            error = True
            print(error)
            print("Echec")
    else:
        form_password = ResetPasswordStep2()

    return render(request, 'yoga_website/reset_password_step.html', {'var_color': var_color, 'admin': admin,
                                                                     'form_password': form_password, 'echec': echec,
                                                                     'utilisateur': utilisateur, "username": username})
