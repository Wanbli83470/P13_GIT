import os
import random
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from .forms import *
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib.auth.models import User
from user_experience.models import Workshop, Client, Inscribe, PdfOutput, SecretCode, PdfInput
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .generate_pdf import ExportPdf
from django.core.exceptions import ValidationError
from django.http import HttpResponse, Http404
from django.urls import reverse

var_color = "vert"
admin = False
mail_soph = os.environ.get("ADRESS_P13_MAIL")


"""Common functions"""


def user_actif(request):

    """Assign a status to the logged in user to modify their functions"""
    list_client = []
    for c in Client.objects.all():
        list_client.append(str(c.user))

    global var_color
    global admin
    my_user = str(request.user)
    user = str
    if request.user.is_superuser:
        var_color = "violet"
        admin = True
        user1 = "admin"
    elif my_user in list_client:
        var_color = "vert"
        user1 = "client"
        admin = False
    elif my_user not in list_client and my_user is not "AnonymousUser" :
        user1 = "client_not_active"
        var_color = "vert"
    elif my_user == "AnonymousUser":
        var_color = "vert"
        user1 = "new_user"
    return user1


def get_id_client(request):
    username = request.user
    client = Client.objects.get(user=username)
    return client.id


def workshop(request):
    """View all workshops : administrator view and user view"""
    if user_actif(request) != "client_not_active":
        user1 = user_actif(request)
        user = request.user
        participants = str
        if user1 == "client":
            client = Client.objects.get(user=user)
            participants = str(Inscribe.objects.filter(client=client))
            participants = [int(l) for l in participants if l.isdecimal()]

        workshops = Workshop.objects.order_by('date')
        if user1 != "admin":
            id_client = get_id_client(request)
        else:
            id_client = 0
        return render(request, 'user_experience/workshop.html', {'workshops': workshops, 'var_color': var_color, 'admin': admin,
                                                              'user1': user1, 'id_client': id_client,
                                                              'participants': participants})
    else:
        return redirect("home")


"""User function"""


def register(request):
    """Registration page for new users"""
    user1 = user_actif(request)
    error = False
    email_used = False
    email_user = User.objects.all()
    email_user1 = []
    for i in email_user:
        print(i.email)
        email_user1.append(i.email)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            messages.success(request, f'Votre compte {username} est crée')
            ExportPdf.generate_pdf(email=email, username=username)
            user_save = User.objects.get(username=username)
            PdfInput(user=user_save, pdf_file=f"user_experience/static/user_experience/formulaire_adhésion_{username}.pdf").save()
            SecretCode(user=user_save).save()
            return redirect("registrationValid", username=username, email=email)
        else:
            error = True
    else:
        form = RegistrationForm()

    return render(request, 'user_experience/register.html', {'form': form, 'var_color': var_color,
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
    email_confirm.attach_file(f"user_experience/static/user_experience/formulaire_adhésion_{username}.pdf")
    email_confirm.send()
    username = str(username)
    return render(request, 'user_experience/registration_valid.html', {'username': username, 'email': email,
                                                                    'var_color': var_color,
                                                                    'admin': admin, 'user1': user1})


def connection(request):
    """Login function with email or username with "authenticate" methods"""
    user1 = user_actif(request)
    error = False
    email_user = User.objects.all()
    email_user1 = []
    for i in email_user:
        print(i.email)
        email_user1.append(i.email)

    if request.method == "POST":
        form = ConnectionForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data["username"]
            print(User.objects.all)
            if username in email_user1:
                print("Détection de mail")
                username = User.objects.get(email=username).username
                print(username)
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # if object is not None
                login(request, user)  # Connect the user
                return redirect('/')
            else:  # A screen error
                error = True
    else:
        form = ConnectionForm()

    return render(request, 'user_experience/connect.html', {'form': form, 'error': error, 'var_color': var_color,
                                                         'admin': admin, 'user1': user1})


def my_espace(request):
    """Personal space to view workshops and see each user's information"""
    user1 = user_actif(request)
    """Update the data user"""
    user = request.user
    path_pdf, registered, nb_registered, id_registered, workshop = None, None, None, None, None
    pdf_input = PdfInput(user=user)
    pdf_input = pdf_input.pdf_file
    pdf_send = False

    """On modifie un client"""
    if user1 == "client":
        client = Client.objects.get(user=user)
        registered = Inscribe.objects.filter(client=client)
        nb_registered = len(registered)
        id_registered = [int(l) for l in str(registered) if l.isdecimal()]
        workshop = Workshop.objects.order_by('date')
        if request.method == "POST":
            user_modif = ClientModif(request.POST or None)
            if user_modif.is_valid():
                username = user_modif.cleaned_data["username"]
                email_adress = user_modif.cleaned_data["email_adress"]
                phone = user_modif.cleaned_data["phone"]
                print(phone)
                user_ = User.objects.get(username=user.username)
                user_.username, user_.email = username, email_adress
                user_.save()
                client.mail_adress = email_adress
                client.Phone = phone
                client.save()
            else:
                print("error")
        else:
            user_modif = ClientModif()

    elif user1 == 'client_not_active':
        try:
            PdfOutput.objects.get(user=user)
            pdf_send = True
        except PdfOutput.DoesNotExist:
            pdf_send = False
        print("on Modifie un client non save")
        client = User.objects.get(username=user.username)
        if request.method == "POST":
            user_modif = UserModif(request.POST or None)
            if user_modif.is_valid():
                username = user_modif.cleaned_data["username"]
                email_adress = user_modif.cleaned_data["email_adress"]
                user_ = User.objects.get(username=user.username)
                user_.username, user_.email = username, email_adress
                user_.save()
            else:
                print("error")
        else:
            user_modif = UserModif()


    """Display of workshops"""
    path_pdf = f"formulaire_adhésion_{request.user.username}.pdf"
    name_pdf = f"formulaire_adhésion_{request.user.username}.pdf"
    pdf_bdd = PdfInput.objects.get(user=user)
    pdf_bdd.save()


    return render(request, "user_experience/my_espace.html", {'var_color': var_color, 'admin': admin,
                                                        'user1': user1, 'name_pdf': name_pdf, 'path_pdf': path_pdf,
                                                        'registered': registered, 'client': client,
                                                        'nb_registered': nb_registered, 'id_registered': id_registered,
                                                        'workshop': workshop, 'user_modif': user_modif,
                                                        'pdf_send': pdf_send, 'pdf_input': pdf_input})


def upload_pdf(request):
    """Page to host the paper form completed by the user"""
    user = request.user
    user1 = user_actif(request)
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
    return render(request, 'user_experience/upload_pdf.html', {'var_color': var_color,
                                                         'form':form, 'user1': user1})


def contact_email(request):
    """Email contact form to speak to the administrator"""
    user1 = user_actif(request)
    form_class = MailForm
    mail_form = form_class(request.POST or None)

    if request.method == "POST":

        if mail_form.is_valid():
            subject = mail_form.cleaned_data["Subject"]
            adresse_mail = mail_form.cleaned_data["mail_adress"]
            body = mail_form.cleaned_data["Body"] + " " + adresse_mail
            email = EmailMessage("Melodyoga : " + subject, body, mail_soph, [mail_soph])

            email.send()
            return redirect('home')

    return render(request, 'user_experience/contact_mail.html', {'mail_form': mail_form, 'var_color': var_color,
                                                         'admin': admin, 'user1': user1})


def inscribe_workshop(request, id_workshop, id_client):
    """Focntion registering a workshop and sending an email to the client"""
    user1 = user_actif(request)

    username = str(request.user)
    email = Client.objects.get(id=id_client)
    email = email.mail_adress
    workshop = Workshop.objects.get(id=id_workshop)
    client = Client.objects.get(id=id_client)
    Inscribe(client=client, workshop=workshop).save()

    subject = f"{username} Votre inscription : Atelier chez Melodyoga"
    adresse_mail = mail_soph
    body = f"Bonjour {username} Nous vous confirmons votre inscription pour l'atelier en date du {workshop.date}, en vous souhaitant une bonne journée."
    email_confirm = EmailMessage(subject, body, adresse_mail, [email, adresse_mail])
    email_confirm.send()

    return render(request, 'user_experience/inscribe_workshop.html', {'var_color': var_color, 'admin': admin, 'user1': user1})


def unsubscribe_workshop(request, id_workshop, id_client):
    """Focntion to unsubscribe a customer from the workshop + confirmation email"""
    user1 = user_actif(request)

    workshop = Workshop.objects.get(id=id_workshop)
    client = Client.objects.get(id=id_client)
    Inscribe.objects.get(client=client, workshop=workshop).delete()

    username = str(request.user)
    email = client.mail_adress

    subject = "Votre déinscription : Atelier chez Melodyoga"
    adresse_mail = mail_soph
    body = f"Bonjour {username} Nous avons bien noté votre annulation pour l'atelier en date du {workshop.date} " \
           f"et espérons vous revoir prochainement."
    email_confirm = EmailMessage(subject, body, adresse_mail, [email, adresse_mail])
    email_confirm.send()

    return render(request, 'user_experience/unsubscribe_workshop.html', {'var_color': var_color,
                                                             'admin': admin, 'user1': user1})

    return redirect('home')


def detail_workshop(request, id_workshop, id_client):
    """Show workshop details and manage registration"""
    if user_actif(request) == "client":
        user1 = user_actif(request)
        id_workshop = id_workshop
        id_client = id_client

        try:
            workshop = Workshop.objects.get(id=id_workshop)
            client = Client.objects.get(id=id_client)
            nb_participants = Inscribe.objects.filter(workshop=workshop)
            nb_participants = len(nb_participants)
            remaining_places = workshop.nb_places - nb_participants
            if remaining_places <= 0:
                places = False
            else:
                places = True
            go_inscribe = True
            try:
                go = Inscribe.objects.get(client=client, workshop=workshop)
                go_inscribe = False
            except Inscribe.DoesNotExist:
                go = None
                go_inscribe = True
            return render(request, 'user_experience/detailAtelier.html',
                          {'var_color': var_color, 'admin': admin, 'user1': user1,
                           'go_inscribe': go_inscribe, 'workshop': workshop, 'id_workshop': id_workshop, 'id_client': id_client,
                           'nb_participants': nb_participants, 'remaining_places': remaining_places, 'places': places})

        except:
            error_404 = "L'assocation ne trouve pas l'atelier que vous cherchez"
            return render(request, 'user_experience/404.html', {'error_404': error_404})

    else:
        return redirect('home')


def disconnection(request):
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
            adresse_mail = form_password.cleaned_data["mail_adress"]

            if username == "" and adresse_mail == "":
                return redirect("reset_password")
            elif username == "":
                username = "null"
            elif adresse_mail == "":
                adresse_mail = "null"

            return redirect("resset_password_step", username=username, email_adress=adresse_mail)
        else:
            error = True
    else:
        form_password = ResetPassword()

    return render(request, 'user_experience/reset_password.html', {'var_color': var_color, 'admin': admin,
                                                                'form_password': form_password})


def reset_password_step_2(request, username, email_adress):
    username, email_adress = username, email_adress
    user, echec, error = None, False, False
    """1) Send the secret code"""
    if username == "null" and email_adress == "null":
        echec = True
    else:
        try:
            user = User.objects.get(email=email_adress)
            secret_entrance = SecretCode.objects.get(user=user)
            """Mail contenant le code secret"""
            subject = "Demande changement du mot de passe sur melodyoga"
            adresse_mail = mail_soph
            body = f"Bonjour {user.username} Voici votre code secret {secret_entrance.code} " \
                   f"Celui-ci vous sera demandé à l'étape suivante pour modifier votre mot de passe"
            email_confirm = EmailMessage(subject, body, adresse_mail, [user.email])
            email_confirm.send()
            username = user.username
        except:
            try:
                user = User.objects.get(username=username)
                secret_entrance = SecretCode.objects.get(user=user)
                """Mail contenant le code secret"""
                subject = "Demande changement du mot de passe sur melodyoga"
                adresse_mail = mail_soph
                body = f"Bonjour {user.username} Voici votre code secret {secret_entrance.code} " \
                       f"Celui-ci vous sera demandé à l'étape suivante pour modifier votre mot de passe"
                email_confirm = EmailMessage(subject, body, adresse_mail, [user.email])
                email_confirm.send()

            except:
                echec = True

    """1) Send the secret code"""
    if request.method == "POST":
        form_password = ResetPasswordStep2(request.POST)

        if form_password.is_valid():
            code = form_password.cleaned_data["code"]
            password = str(form_password.cleaned_data["password"])
            error = False
            if str(code) == str(secret_entrance.code):
                user.set_password(password)
                user.save()
                """On attribue un nouveau code secret pour l'avenir"""
                code_secret = str(random.randint(10000, 100000))
                secret_entrance = SecretCode.objects.get(user=user)
                secret_entrance.code = str(code_secret)
                secret_entrance.save()

                """Confirmation changement de mot de passe"""
                subject = "Mot de passe modifié Melodyoga"
                adresse_mail = mail_soph
                body = f"{user.username} Nous vous confirmons le changement de mot de passe " \
                       f"suite à votre procédure sur notre site"
                email_confirm = EmailMessage(subject, body, adresse_mail, [user.email, adresse_mail])
                email_confirm.send()

                """Redirection"""
                return redirect("home")
            else:
                error = True
        else:
            error = True
    else:
        form_password = ResetPasswordStep2()

    return render(request, 'user_experience/reset_password_step.html', {'var_color': var_color, 'admin': admin,
                                                                     'form_password': form_password, 'echec': echec,
                                                                     "username": username, 'error': error})


def delete_account(request):
    """User delete function. With the elimination of workshops and data attached to the client"""
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
        user_account = Client.objects.get(user=user)
        for i in Inscribe.objects.filter(client=user_account):
            i.delete()
        user_account.delete()
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
