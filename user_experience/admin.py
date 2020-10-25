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
    list_display = ('first_name', 'Phone', 'mail_adress')
    list_filter = ('first_name',)
    ordering = ('first_name',)
    search_fields = ('mail_adress', 'first_name', 'last_name')


class InscribeAdmin(admin.ModelAdmin):
    list_display = ('client', 'workshop')
    list_filter = ('client',)
    ordering = ('client',)


class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('type', 'nb_places', 'date', 'location', 'places')
    list_filter = ('type',)
    date_hierarchy = 'date'
    ordering = ('nb_places',)
    search_fields = ('type', 'location')


admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Inscribe, InscribeAdmin)
admin.site.register(PdfInput, PdfAdmin)
admin.site.register(PdfOutput, PdfAdmin)
admin.site.register(SecretCode, SecretAdmin)

