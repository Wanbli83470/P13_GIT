from django.shortcuts import render, redirect
from user_experience.models import *
from user_experience.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    )
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
    if request.user.is_superuser:
        var_color = "violet"
        admin = True
        user1 = "admin"
    elif mon_user in list_client:
        var_color = "vert"
        user1 = "client"
        admin = False
    elif mon_user not in list_client and mon_user is not "AnonymousUser":
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
        return render(request, 'user_experience/404.html', {'error_404': error_404})

    select_participants = Inscribe.objects.filter(workshop=select_atelier)
    nb_participants = len(select_participants)
    places_restantes = select_atelier.nb_places - nb_participants
    return render(request, 'administration/participants.html', {'var_color': var_color, 'admin': admin, 'user1': user1,
                                                              'id_atelier': id_atelier,
                                                              "select_participants": select_participants,
                                                              "select_atelier": select_atelier,
                                                              'places_restantes': places_restantes,
                                                              'nb_participants': nb_participants})


def delete_workshop(request, id_workshop):
    user1 = user_actif(request)
    Workshop(id=id_workshop).delete()
    return render(request, 'user_experience/workshop.html', {'var_color': var_color, 'admin': admin, 'user1': user1})


def clients(request):
    user1 = user_actif(request)
    client = Client.objects.all()
    print(client)
    if request.method == "POST":
        form = ClientsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients')
        else:
            error = True
    else:
        form = ClientsForm()

    return render(request, 'administration/clients.html', {"client": client, "form": form, 'var_color': var_color,
                                                         'admin': admin, 'user1': user1})


class CreateAteliersView(LoginRequiredMixin, CreateView):
    model = Workshop
    fields = ['type', 'nb_places', 'date', 'location', 'places']
    template_name = 'administration/atelier_form.html'
