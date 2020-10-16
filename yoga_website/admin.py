from django.contrib import admin
from .models import Atelier, Client, Inscribe, Pdf, SecretCode
# Register your models here.

class SecretAdmin(admin.ModelAdmin):
    list_display = ('user', 'code')
    list_filter = ('user', 'code',)
    ordering = ('user',)
    search_fields = ('user', 'code')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'tel', 'email')
    list_filter = ('prenom',)
    date_hierarchy = 'date'
    ordering = ('prenom',)
    search_fields = ('email', 'prenom', 'nom')

admin.site.register(Atelier)
admin.site.register(Client, ClientAdmin)
admin.site.register(Inscribe)
admin.site.register(Pdf)
admin.site.register(SecretCode, SecretAdmin)

