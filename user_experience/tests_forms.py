from django.test import SimpleTestCase
from user_experience.forms import *
# Create your tests here.


class TestForms(SimpleTestCase):

    def test_mail_form_valid(self):
        form_mail = MailForm(data={
            'Subject': 'Test email',
            'mail_adress': 'estival.t@hotmail.com',
            'Body': "Un mail à l'attention de l'admin"
        })
        self.assertTrue(form_mail.is_valid())

    def test_mail_form_invalid(self):
        form_mail = MailForm(data={
            'Subject': 'Test email',
            'mail_adress': 'André',
            'Body': "Un mail à l'attention de l'admin"
        })
        self.assertFalse(form_mail.is_valid())
        self.assertEqual(len(form_mail.errors), 1)

    def test_reset_password_mail(self):
        form_password = ResetPassword(data={
            'mail_adress': 'oc@gmail.com',
            'username': '',
        })
        self.assertTrue(form_password.is_valid())

    def test_reset_password_username(self):
        form_password = ResetPassword(data={
            'mail_adress': '',
            'username': 'OC_USER',
        })
        self.assertTrue(form_password.is_valid())

    def test_reset_password_step(self):
        form_password_step = ResetPasswordStep2(data={
            'password': 'lhjtufgod%85',
            'code': '65894',
        })
        self.assertTrue(form_password_step.is_valid())

    def test_reset_password_step_invalide_code(self):
        form_password_step = ResetPasswordStep2(data={
            'password': 'lhjtufgod%85',
            'code': '6589456',
        })
        self.assertFalse(form_password_step.is_valid())