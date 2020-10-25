from django.test import TestCase
from user_experience.models import Workshop


class WorkShopModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Workshop.objects.create(type='YOGA_TEST', nb_places=5, places=True, location="Brignoles")

    def test_first_name_label(self):
        Workshop_1 = Workshop.objects.get(id=1)
        field_label = Workshop_1._meta.get_field('type').verbose_name
        self.assertEquals(field_label, 'type')

    def test_location_max_length(self):
        Workshop_1 = Workshop.objects.get(id=1)
        max_length = Workshop_1._meta.get_field('location').max_length
        self.assertEquals(max_length, 50)

    def test_places_default_true(self):
        Workshop_1 = Workshop.objects.get(id=1)
        default_true = Workshop_1._meta.get_field('places').default
        self.assertEquals(default_true, True)

