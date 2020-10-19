from django.contrib import admin
from .models import *
# Register your models here.

class PdfAdmin(admin.ModelAdmin):
    list_display = ('user', 'pdf_file')
    list_filter = ('user',)
    ordering = ('user',)

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

class InscribeAdmin(admin.ModelAdmin):
    list_display = ('client', 'atelier')
    list_filter = ('client',)
    ordering = ('client',)

class AtelierAdmin(admin.ModelAdmin):
    list_display = ('type', 'nb_places', 'date', 'lieux', 'places')
    list_filter = ('type',)
    date_hierarchy = 'date'
    ordering = ('nb_places',)
    search_fields = ('type', 'lieux')


admin.site.register(Atelier, AtelierAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Inscribe, InscribeAdmin)
admin.site.register(PdfInput, PdfAdmin)
admin.site.register(PdfOutput, PdfAdmin)
admin.site.register(SecretCode, SecretAdmin)

