from django.contrib import admin
from .models import Atelier, Client, Inscribe, Pdf, SecretCode
# Register your models here.
admin.site.register(Atelier)
admin.site.register(Client)
admin.site.register(Inscribe)
admin.site.register(Pdf)
admin.site.register(SecretCode)
