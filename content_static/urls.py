from django.urls import path

from. import views
urlpatterns = [
    path('', views.home, name="home"),
    path('yoga', views.yoga, name="yoga"),
    path('music', views.music_therapy, name="music_therapy"),
    path('nidra', views.nidra, name="nidra"),
]
