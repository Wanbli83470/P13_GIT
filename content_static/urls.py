from django.urls import path


from user_experience.views import (AtelierListView,
                                   CreateAteliersView,
                                   )

from. import views
urlpatterns = [
    path('yoga', views.yoga, name="yoga"),
    path('video', views.video, name="video"),
    path('nidra', views.nidra, name="nidra"),

]
