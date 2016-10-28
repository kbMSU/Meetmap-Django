from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

class LoginTestCase(TestCase):
    test_client = None

    def setUp(self):
        self.test_client = Client()

    def test_get_login_page_success(self):
        response = self.test_client.get('/')

        # Assert that the page was returned successfully
        self.assertEqual(response.status_code,200)

    def test_login_success(self):
        newUser = User.objects.create_user("test", "test@test.com", "test1234")
        newUser.save()
        response = self.test_client.post('/', {'username':'test', 'password':'test1234'})

        # Assert that the page was redirected away after successful login
        self.assertEqual(response.status_code,302)

    def test_login_failed(self):
        response = self.test_client.post('/', {'username': 'john', 'password': 'smith'})

        # Assert that the loginFailed variable is True
        self.assertTrue(response.context['loginFailed'])

        # Assert that the page was returned successfully
        self.assertEqual(response.status_code,200)

    def test_login_username_missing(self):
        response = self.test_client.post('/', {'username':'', 'password': 'smith'})

        # Assert that the usernameMissing variable is True
        self.assertTrue(response.context['usernameMissing'])

        # Assert that the page was returned successfully
        self.assertEqual(response.status_code,200)

    def test_password_missing(self):
        response = self.test_client.post('/', {'username': 'john', 'password':''})

        # Assert that the passwordMissing variable is True
        self.assertTrue(response.context['passwordMissing'])

        # Assert that the page was returned successfully
        self.assertEqual(response.status_code,200)

class SignupTestCase(TestCase)
    test_client = None

    def setUp(self):
        self.test_client = Client()
