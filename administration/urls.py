from django.urls import path


from yoga_website.views import (AtelierListView,
                                CreateAteliersView,
                                )

from. import views
urlpatterns = [
    path('participants/<int:id_atelier>', views.participants, name="participants"),
    path('deleteAtelier/<int:id_atelier>', views.delete_atelier, name="deleteAtelier"),
    path('clients', views.clients, name="clients"),

]
