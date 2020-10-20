from django.shortcuts import render, redirect
from yoga_website.models import *
from yoga_website.forms import *
var_color = "vert"
admin = False


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
# Create your views here.


def participants(request, id_atelier):
    user1 = user_actif(request)
    if user1 != "admin":
        return redirect('home')

    try:
        select_atelier = Workshop.objects.get(id=id_atelier)
    except:
        error_404 = "Atelier introuvable à cet identifiant"
        return render(request, 'yoga_website/404.html', {'error_404': error_404})

    select_participants = Inscribe.objects.filter(workshop=select_atelier)
    nb_participants = len(select_participants)
    places_restantes = select_atelier.nb_places - nb_participants
    return render(request, 'administration/participants.html', {'var_color': var_color, 'admin': admin, 'user1': user1,
                                                              'id_atelier': id_atelier,
                                                              "select_participants": select_participants,
                                                              "select_atelier": select_atelier,
                                                              'places_restantes': places_restantes,
                                                              'nb_participants': nb_participants})


def delete_atelier(request, id_atelier):
    user1 = user_actif(request)
    Workshop(id=id_atelier).delete()
    return render(request, 'yoga_website/ateliers.html', {'var_color': var_color, 'admin': admin, 'user1': user1})


def clients(request):
    user1 = user_actif(request)
    client = Client.objects.all()
    if request.method == "POST":
        form = ClientsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients')
        else:
            error = True
    else:
        form = ClientsForm(request.POST)

    return render(request, 'administration/clients.html', {"client": client, "form": form, 'var_color': var_color,
                                                         'admin': admin, 'user1': user1})

