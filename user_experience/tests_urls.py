from django.test import SimpleTestCase
from django.urls import reverse, resolve
from content_static.views import yoga, music_therapy, nidra, error_404_view
from administration.views import participants, clients, delete_workshop, CreateAteliersView
from user_experience.views import *


class TestUrls(SimpleTestCase):
    print("Test des urls")
    def test_list_url_static(self):
        url_yoga = reverse("yoga")
        url_music = reverse("music_therapy")
        url_nidra = reverse("nidra")
        url_client = reverse("clients")
        url_new_atelier = reverse("create-atelier")
        url_workshop = reverse("workshop")
        url_register = reverse("register")
        url_connection = reverse("connection")
        url_my_espace = reverse("espace")
        url_upload_pdf = reverse("upload_pdf")
        url_contact_email = reverse("mail_contact")
        url_deleteAccount = reverse("delete_account")
        url_reset_password = reverse("reset_password")
        url_disconnection = reverse("disconnection")
        self.assertEqual(resolve(url_yoga).func, yoga)
        self.assertEqual(resolve(url_music).func, music_therapy)
        self.assertEqual(resolve(url_nidra).func, nidra)
        self.assertEqual(resolve(url_client).func, clients)
        self.assertEqual(resolve(url_new_atelier).func.view_class, CreateAteliersView)
        self.assertEqual(resolve(url_workshop).func, workshop)
        self.assertEqual(resolve(url_register).func, register)
        self.assertEqual(resolve(url_connection).func, connection)
        self.assertEqual(resolve(url_my_espace).func, my_espace)
        self.assertEqual(resolve(url_upload_pdf).func, upload_pdf)
        self.assertEqual(resolve(url_contact_email).func, contact_email)
        self.assertEqual(resolve(url_deleteAccount).func, delete_account)
        self.assertEqual(resolve(url_reset_password).func, reset_password)
        self.assertEqual(resolve(url_disconnection).func, disconnection)

    def test_args_urls(self):
        url_participants = reverse("participants", args=[5])
        url_delete_workshop = reverse("deleteWorkshop", args=[2])
        url_inscribe_workshop = reverse("inscribe", args=[1, 1])
        url_unsubscribe_workshop = reverse("unsubscribe", args=[1, 1])
        url_registration_valid = reverse("registrationValid", args=["OC_USER", "oc@gmail.com"])
        url_resset_password_step = reverse("resset_password_step", args=["OC_USER", "oc@gmail.com"])

        self.assertEqual(resolve(url_participants).func, participants)
        self.assertEqual(resolve(url_delete_workshop).func, delete_workshop)
        self.assertEqual(resolve(url_inscribe_workshop).func, inscribe_workshop)
        self.assertEqual(resolve(url_unsubscribe_workshop).func, unsubscribe_workshop)
        self.assertEqual(resolve(url_registration_valid).func, registration_valid)
        self.assertEqual(resolve(url_resset_password_step).func, reset_password_step_2)
