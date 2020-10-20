from django.urls import path


from user_experience.views import (AtelierListView,
                                   CreateAteliersView,
                                   )

from. import views
urlpatterns = [
    path('participants/<int:id_atelier>', views.participants, name="participants"),
    path('deleteWorkshop/<int:id_workshop>', views.delete_workshop, name="deleteWorkshop"),
    path('clients', views.clients, name="clients"),

]
