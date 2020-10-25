from django.test import SimpleTestCase
from django.urls import reverse, resolve
from content_static.views import yoga, music_therapy, nidra, error_404_view
from administration.views import participants, clients

class TestUrls(SimpleTestCase):

    def test_list_url_static(self):
        url_yoga = reverse("yoga")
        url_music = reverse("music_therapy")
        url_nidra = reverse("nidra")
        url_client = reverse("clients")
        self.assertEqual(resolve(url_yoga).func, yoga)
        self.assertEqual(resolve(url_music).func, music_therapy)
        self.assertEqual(resolve(url_nidra).func, nidra)
        self.assertEqual(resolve(url_client).func, clients)

    def test_args_urls(self):
        url_participants = reverse("participants", args=[5])
        self.assertEqual(resolve(url_participants).func, participants)