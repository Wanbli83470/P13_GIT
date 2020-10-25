from django.test import TestCase
from django.urls import reverse

class StaticViewsTest(TestCase):
    print("Test des templates htmls accéssibles à tout le monde")

    def test_static_html_return(self):
        home_html = self.client.get(reverse('home'))
        yoga_html = self.client.get(reverse('yoga'))
        music_html = self.client.get(reverse('music_therapy'))
        nidra_html = self.client.get(reverse('nidra'))
        connection_html = self.client.get(reverse('connection'))
        register_html = self.client.get(reverse('register'))

        self.assertEqual(home_html.status_code, 200)
        self.assertTemplateUsed(home_html, "content_static/home.html")

        self.assertEqual(yoga_html.status_code, 200)
        self.assertTemplateUsed(yoga_html, 'content_static/yoga.html')

        self.assertEqual(music_html.status_code, 200)
        self.assertTemplateUsed(music_html, "content_static/music_therapy.html")

        self.assertEqual(nidra_html.status_code, 200)
        self.assertTemplateUsed(nidra_html, "content_static/nidra.html")

        self.assertEqual(connection_html.status_code, 200)
        self.assertTemplateUsed(connection_html, 'user_experience/connect.html')

        self.assertEqual(register_html.status_code, 200)
        self.assertTemplateUsed(register_html, 'user_experience/register.html')



    def test_html_404_return(self):
        html_404 = self.client.get('/page/azertyui')
        self.assertEqual(html_404.status_code, 404)
        self.assertTemplateUsed(html_404, 'content_static/404.html')
