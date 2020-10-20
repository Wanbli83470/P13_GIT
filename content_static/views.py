from django.shortcuts import render
from user_experience.models import *

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


"""HTTP request errors function"""


def error_404_view(request, exception):
    return render(request, 'content_static/404.html', status=404)


def error_500_view(request, *args):
    return render(request, 'content_static/500.html')


"""Static functions"""


def yoga(request):
    user1 = user_actif(request)
    return render(request, "content_static/yoga.html", {'var_color': var_color,
                                                      'admin': admin, 'user1': user1})


def nidra(request):
    user1 = user_actif(request)
    return render(request, "content_static/nidra.html", {'video': video, 'var_color': var_color,
                                                       'user1': user1})


def video(request):
    user1 = user_actif(request)
    video = True
    return render(request, "content_static/vidéo.html", {'video': video, 'var_color': var_color,
                                                       'admin': admin, 'user1': user1})
