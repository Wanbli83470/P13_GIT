import os
import random
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from .forms import *
from .quote import quote_day
from django.core.mail import EmailMessage
from django.urls import reverse
from django.views.generic import (
    ListView,
    CreateView,
    )
from django.contrib.auth.models import User
from yoga_website.models import Workshop, Client, Inscribe, PdfOutput, SecretCode, PdfInput
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .generate_pdf import generate_pdf
from django.http import HttpResponse, Http404
from django.urls import reverse

var_color = "vert"
admin = False
mail_soph = os.environ.get("ADRESS_P13_MAIL")


"""Common functions"""


def user_actif(request):
    list_client = []
    for c in Client.objects.all():
        list_client.append(str(c.user))

    global var_color
    global admin
    mon_user = str(request.user)
    user = str
    if mon_user == "thomas":
        var_color = "violet"
        admin = True
        user1 = "admin"
    elif mon_user in list_client:
        var_color = "vert"
        user1 = "client"
        admin = False
    elif mon_user not in list_client and mon_user is not "AnonymousUser" :
        user1 = "client_not_active"
        var_color = "vert"
    elif mon_user == "AnonymousUser":
        var_color = "vert"
        user1 = "new_user"
    return user1


def home(request):
    user1 = user_actif(request)
    return render(request, "yoga_website/bienvenu.html", {'quote_day': quote_day,
                                                          'var_color': var_color, 'admin': admin, 'user1': user1})


def ateliers(request):
    """View all workshops : administrator view and user view"""
    if user_actif(request) != "client_not_active":
        user1 = user_actif(request)
        user = request.user
        participants = str
        if user1 == "client":
            client = Client.objects.get(user=user)
            participants = str(Inscribe.objects.filter(client=client))
            participants = [int(l) for l in participants if l.isdecimal()]

        ateliers = Workshop.objects.order_by('date')
        if user1 != "admin":
            id_client = get_id_client(request)
        else:
            id_client = 0
        return render(request, 'yoga_website/ateliers.html', {'ateliers': ateliers, 'var_color': var_color, 'admin': admin,
                                                              'user1': user1, 'id_client': id_client,
                                                              'participants': participants})
    else:
        return redirect("home")


"""Administrator's function"""


def get_id_client(request):
    username = request.user
    client = Client.objects.get(user=username)
    return client.id


class CreateAteliersView(LoginRequiredMixin, CreateView):
    model = Workshop
    fields = ['type', 'nb_places', 'date', 'location', 'places']
    template_name = 'yoga_website/atelier_form.html'


"""User function"""


def register(request):
    """Registration page for new users"""
    user1 = user_actif(request)
    error = False
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            messages.success(request, f'Votre compte {username} est crée')
            generate_pdf(email=email, username=username)
            user_save = User.objects.get(username=username)
            PdfInput(user=user_save, pdf_file=f"yoga_website/static/yoga_website/formulaire_adhésion_{username}.pdf").save()
            SecretCode(user=user_save).save()
            return redirect("registrationValid", username=username, email=email)
        else:
            error = True
    else:
        form = RegistrationForm(request.POST)

    return render(request, 'yoga_website/register.html', {'form': form, 'var_color': var_color,
                                                          'admin': admin, 'user1': user1})


def registration_valid(request, username, email):

    """HTML confirmation page following a registration"""
    user1 = user_actif(request)
    subject = "Votre inscription sur melodyoga"
    adresse_mail = mail_soph
    body = f"Bonjour {username} Nous vous confirmons votre inscription sur Melodyoga, " \
           f"Vous trouverez ci-joint un formulaire papier à nous renvoyer signé" \
           f" afin d'enregistrer définitivement votre inscription à notre association " \
           f"en vous souhaitant une bonne journée"
    email_confirm = EmailMessage(subject, body, adresse_mail, [email, adresse_mail])
    email_confirm.content_subtype = "html"
    email_confirm.attach_file(f"yoga_website/static/yoga_website/formulaire_adhésion_{username}.pdf")
    email_confirm.send()
    username = str(username)
    return render(request, 'yoga_website/registration_valid.html', {'username': username, 'email': email,
                                                                    'var_color': var_color,
                                                                    'admin': admin, 'user1': user1})


def connexion(request):
    user1 = user_actif(request)
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                return redirect('/')
            else:  # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'yoga_website/connect.html', {'form': form, 'error': error, 'var_color': var_color,
                                                         'admin': admin, 'user1': user1})


def my_espace(request):
    user1 = user_actif(request)
    """Update the data user"""
    user_modif = UserModif()
    user = request.user
    chemin_pdf, registered, client, nb_registered, id_registered, ateliers = None, None, None, None, None, None
    pdf_input = PdfInput(user=user)
    pdf_input = pdf_input.pdf_file
    pdf_send = False
    if user1 != "admin":
        if user1 == "client_not_active":
            try:
                pdf_send = PdfOutput.objects.get(user=user)
                pdf_send = True
            except PdfOutput.DoesNotExist:
                pdf_send = False
            if request.method == "POST":
                user_modif = UserModif(request.POST)
                if user_modif.is_valid():
                    username = user_modif.cleaned_data["username"]
                    adresse_mail = user_modif.cleaned_data["adresse_mail"]
                    password = user_modif.cleaned_data["password"]
                else:
                    error = True

        elif user1 == "client":
            client = Client.objects.get(user=user)
            if user_modif.is_valid():
                username = user_modif.cleaned_data["username"]
                adresse_mail = user_modif.cleaned_data["adresse_mail"]
                password = user_modif.cleaned_data["password"]
                phone = user_modif.cleaned_data["phone"]
                """Modif"""
                client.phone = phone
                client.mail_adress = adresse_mail
                user.set_password(password)
                user.username = username
                user.email = adresse_mail
                user.save()
                client.save()

        else:
            user_modif = UserModif()


        """Display of workshops"""
        chemin_pdf = f"formulaire_adhésion_{request.user.username}.pdf"
        name_pdf = f"formulaire_adhésion_{request.user.username}.pdf"
        pdf_bdd = PdfInput.objects.get(user=user)
        pdf_bdd.save()
        registered = Inscribe.objects.filter(client=client)
        nb_registered = len(registered)
        id_registered = [int(l) for l in str(registered) if l.isdecimal()]
        ateliers = Workshop.objects.order_by('date')
        id_ateliers = [i.id for i in ateliers]
    else:
        pass
    return render(request, "yoga_website/espace.html", {'var_color': var_color, 'admin': admin,
                                                        'user1': user1, 'name_pdf': name_pdf, 'chemin_pdf': chemin_pdf,
                                                        'registered': registered, 'client': client,
                                                        'nb_registered': nb_registered, 'id_registered': id_registered,
                                                        'ateliers': ateliers, 'user_modif': user_modif,
                                                        'pdf_send': pdf_send, 'pdf_input': pdf_input})


def upload_file(request):
    user = request.user
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_save = PdfOutput()
            pdf_save.user = user
            pdf_save.pdf_file = request.FILES['pdf_file']
            pdf_save.save()
            return redirect('home')
        else:
            pass
    else:
        form = UploadFileForm()
    return render(request, 'yoga_website/upload.html', {'form': form})


def contact_email(request):
    user1 = user_actif(request)
    form_class = MailForm
    mail_form = form_class(request.POST or None)

    if request.method == "POST":

        if mail_form.is_valid():
            subject = mail_form.cleaned_data["subject"]
            adresse_mail = mail_form.cleaned_data["adresse_mail"]
            body = mail_form.cleaned_data["body"] + " " + adresse_mail
            email = EmailMessage("Melodyoga : " + subject, body, mail_soph, [mail_soph])

            email.send()
            return redirect('/home')

    return render(request, 'yoga_website/contact.html', {'mail_form': mail_form, 'var_color': var_color,
                                                         'admin': admin, 'user1': user1})


def inscribe(request, id_atelier, id_client):
    user1 = user_actif(request)

    username = str(request.user)
    email = Client.objects.get(id=id_client)
    email = email.email

    atelier = Workshop.objects.get(id=id_atelier)
    client = Client.objects.get(id=id_client)
    Inscribe(client=client, workshop=atelier).save()

    subject = f"{username} Votre inscription : Atelier chez Melodyoga"
    adresse_mail = mail_soph
    body = f"Bonjour {username} Nous vous confirmons votre inscription pour l'atelier en date du {atelier.date}, en vous souhaitant une bonne journée."
    email_confirm = EmailMessage(subject, body, adresse_mail, [email, adresse_mail])
    email_confirm.send()

    return render(request, 'yoga_website/inscribe.html', {'var_color': var_color, 'admin': admin, 'user1': user1})


def unsubscribe(request, id_atelier, id_client):
    user1 = user_actif(request)

    atelier = Workshop.objects.get(id=id_atelier)
    client = Client.objects.get(id=id_client)
    Inscribe.objects.get(client=client, workshop=atelier).delete()

    username = str(request.user)
    email = client.email

    subject = "Votre déinscription : Atelier chez Melodyoga"
    adresse_mail = mail_soph
    body = f"Bonjour {username} Nous avons bien noté votre annulation pour l'atelier en date du {atelier.date} " \
           f"et espérons vous revoir prochainement."
    email_confirm = EmailMessage(subject, body, adresse_mail, [email, adresse_mail])
    email_confirm.send()

    return render(request, 'yoga_website/unsubscribe.html', {'var_color': var_color,
                                                             'admin': admin, 'user1': user1})

    return redirect('home')


def detail_atelier(request, idatelier, idclient):
    """Show workshop details and manage registration"""
    if user_actif(request) == "client":
        user1 = user_actif(request)
        id_atelier = idatelier
        id_client = idclient

        try:
            atelier = Workshop.objects.get(id=id_atelier)
            client = Client.objects.get(id=id_client)
            nb_participants = Inscribe.objects.filter(workshop=atelier)
            nb_participants = len(nb_participants)
            places_restantes = atelier.nb_places - nb_participants
            if places_restantes <= 0:
                places = False
            else:
                places = True
            go_inscribe = True
            try:
                go = Inscribe.objects.get(client=client, workshop=atelier)
                go_inscribe = False
            except Inscribe.DoesNotExist:
                go = None
                go_inscribe = True
            return render(request, 'yoga_website/detailAtelier.html',
                          {'var_color': var_color, 'admin': admin, 'user1': user1,
                           'go_inscribe': go_inscribe, 'atelier': atelier, 'id_atelier': id_atelier, 'id_client': id_client,
                           'nb_participants': nb_participants, 'places_restantes': places_restantes, 'places': places})

        except:
            error_404 = "L'assocation ne trouve pas l'atelier que vous cherchez"
            return render(request, 'yoga_website/404.html', {'error_404': error_404})

    else:
        return redirect('home')


class AtelierListView(ListView):
    model = Workshop
    template_name = 'yoga_website/ateliers.html'
    context_object_name = "ateliers"


def deconnexion(request):
    user1 = user_actif(request)
    global var_color
    global admin
    logout(request)
    var_color = "vert"
    admin = False
    return redirect('home')


def reset_password(request):

    if request.method == "POST":
        form_password = ResetPassword(request.POST)

        if form_password.is_valid():
            username = form_password.cleaned_data["username"]
            adresse_mail = form_password.cleaned_data["adresse_mail"]
            if username == "":
                username = "null"
            if adresse_mail == "":
                adresse_mail = "null"
            return redirect("resset_password_step", username=username, adresse_mail=adresse_mail,)
        else:
            error = True
    else:
        form_password = ResetPassword()

    return render(request, 'yoga_website/reset_password.html', {'var_color': var_color, 'admin': admin,
                                                                'form_password': form_password})


def reset_password_step_2(request, username, adresse_mail):
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
            subject = "Demande changement du mot de passe sur melodyoga"
            adresse_mail = mail_soph
            body = f"Bonjour {utilisateur.username} Voici votre code secret {secret_entrance.code} " \
                   f"Celui-ci vous sera demandé à l'étape suivante pour modifier votre mot de passe"
            email_confirm = EmailMessage(subject, body, adresse_mail, [utilisateur.email])
            email_confirm.send()
            username = utilisateur.username
        except:
            try:
                utilisateur = User.objects.get(username=username)
                secret_entrance = SecretCode.objects.get(user=utilisateur)
                """Mail contenant le code secret"""
                subject = "Demande changement du mot de passe sur melodyoga"
                adresse_mail = mail_soph
                body = f"Bonjour {utilisateur.username} Voici votre code secret {secret_entrance.code} " \
                       f"Celui-ci vous sera demandé à l'étape suivante pour modifier votre mot de passe"
                email_confirm = EmailMessage(subject, body, adresse_mail, [utilisateur.email])
                email_confirm.send()

            except:
                echec = True

    if request.method == "POST":
        form_password = ResetPasswordStep2(request.POST)

        if form_password.is_valid():
            code = form_password.cleaned_data["code"]
            password = str(form_password.cleaned_data["password"])

            if str(code) == str(secret_entrance.code):
                utilisateur.set_password(password)
                utilisateur.save()
                """On attribue un nouveau code secret pour l'avenir"""
                code_secret = str(random.randint(10000, 100000))
                secret_entrance = SecretCode.objects.get(user=utilisateur)
                secret_entrance.code = str(code_secret)
                secret_entrance.save()

                """Confirmation changement de mot de passe"""
                subject = "Mot de passe modifié Melodyoga"
                adresse_mail = mail_soph
                body = f"{utilisateur.username} Nous vous confirmons le changement de mot de passe " \
                       f"suite à votre procédure sur notre site"
                email_confirm = EmailMessage(subject, body, adresse_mail, [utilisateur.email])
                email_confirm.send()

                """Redirection"""
                return redirect("home")

            else:
                pass

        else:
            error = True
    else:
        form_password = ResetPasswordStep2()

    return render(request, 'yoga_website/reset_password_step.html', {'var_color': var_color, 'admin': admin,
                                                                     'form_password': form_password, 'echec': echec,
                                                                     'utilisateur': utilisateur, "username": username})


def delete_compte(request):
    user = request.user
    user1 = user_actif(request)

    """Supprimer tous les liens avec clef étrangères : """
    try:
        SecretCode.objects.get(user=user).delete()
    except SecretCode.DoesNotExist:
        pass

    try:
        PdfInput.objects.get(user=user).delete()
    except PdfInput.DoesNotExist:
        pass

    try:
        PdfOutput.objects.get(user=user).delete()
    except PdfOutput.DoesNotExist:
        pass

    """Supprimer les inscriptions aux ateliers"""
    if user1 == "client":
        compte_delete = Client.objects.get(user=user)
        for i in Inscribe.objects.filter(client=compte_delete):
            i.delete()
        compte_delete.delete()
        user.delete()

    else:
        user.delete()

    """Mail de confirmation"""
    subject = "Suppresion de votre compte sur melodyoga"
    adresse_mail = mail_soph
    body = f"Bonjour {user.username} Nous vous confirmons suppresion de votre compte sur melodyoga, " \
           f"En vous souhaitant une bonne journée"
    email_confirm = EmailMessage(subject, body, adresse_mail, [user.email, adresse_mail])
    email_confirm.send()


    return redirect('home')