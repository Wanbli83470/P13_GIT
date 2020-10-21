from django.urls import path

from administration.views import CreateAteliersView

from. import views
urlpatterns = [
    path('participants/<int:id_atelier>', views.participants, name="participants"),
    path('deleteWorkshop/<int:id_workshop>', views.delete_workshop, name="deleteWorkshop"),
    path('clients', views.clients, name="clients"),
    path('new-atelier/', CreateAteliersView.as_view(), name="create-atelier"),
]
