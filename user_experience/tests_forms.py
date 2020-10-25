from django.test import SimpleTestCase
from user_experience.forms import *
from user_experience.models import *
# Create your tests here.


class TestForms(SimpleTestCase):
    print("Test des formulaire")


    """Form testing"""
    def test_mail_form_valid(self):
        """Testing the correct email form"""
        form_mail = MailForm(data={
            'Subject': 'Test email',
            'mail_adress': 'estival.t@hotmail.com',
            'Body': "Un mail à l'attention de l'admin"
        })
        self.assertTrue(form_mail.is_valid())

    def test_mail_form_invalid(self):
        """Testing the incorrect email form :
        Wrong syntax of the email address"""
        form_mail = MailForm(data={
            'Subject': 'Test email',
            'mail_adress': 'André',
            'Body': "Un mail à l'attention de l'admin"
        })
        self.assertFalse(form_mail.is_valid())
        self.assertEqual(len(form_mail.errors), 1)

    def test_reset_password_mail(self):
        """1st step Reset password form test by mail"""
        form_password = ResetPassword(data={
            'mail_adress': 'oc@gmail.com',
            'username': '',
        })
        self.assertTrue(form_password.is_valid())

    def test_reset_password_username(self):
        """1st step Reset password form test by username"""
        form_password = ResetPassword(data={
            'mail_adress': '',
            'username': 'OC_USER',
        })
        self.assertTrue(form_password.is_valid())

    def test_reset_password_step(self):
        """1st step Reset password form test by username"""
        form_password_step = ResetPasswordStep2(data={
            'password': 'lhjtufgod%85',
            'code': '65894',
        })
        self.assertTrue(form_password_step.is_valid())

    def test_reset_password_step_invalide_code(self):
        """Testing 2nd step the Reset password form with an invalid code"""
        form_password_step = ResetPasswordStep2(data={
            'password': 'lhjtufgod%85',
            'code': '6589456',
        })
        self.assertFalse(form_password_step.is_valid())

"""
    def test_client_modif(self):

        form_client_modif = ClientModif(data={
            'username': 'OC_USER3',
            'email_adress': 'oc@gmail.com',
            'phone': '0771591021'
        })
        self.assertTrue(form_client_modif.is_valid())

"""