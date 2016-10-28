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

class SignupTestCase(TestCase):
    test_client = None

    def setUp(self):
        self.test_client = Client()

    def test_get_signup_page_success(self):
        response = self.test_client.get('/signup/')

        # Assert that the page was returned successfully
        self.assertEqual(response.status_code,200)

    def test_signup_success(self):
        response = self.test_client.post('/signup/',
                    {'username':'test','password1':'pass1234',
                    'password2':'pass1234','email':'test@test.com'})

        # Assert that registration succeeded
        self.assertTrue(response.context['registerSuccess'])

        # Assert that the page was returned successfully
        self.assertEqual(response.status_code,200)

    def test_signup_username_exists(self):
        newUser = User.objects.create_user("test", "test@test.com", "test1234")
        newUser.save()

        response = self.test_client.post('/signup/',
                    {'username':'test','password1':'pass1234',
                    'password2':'pass1234','email':'test@test.com'})

        # Assert that registration failed
        self.assertFalse(response.context['registerSuccess'])

        # Assert that the username already exists
        self.assertTrue(response.context['usernameExists'])

        # Assert that the page was returned successfully
        self.assertEqual(response.status_code,200)

    def test_signup_password_too_short(self):
        response = self.test_client.post('/signup/',
                    {'username':'test','password1':'p',
                    'password2':'p','email':'test@test.com'})

        # Assert that registration failed
        self.assertFalse(response.context['registerSuccess'])

        # Assert that password is too short
        self.assertTrue(response.context['passwordTooShort'])

        # Assert that the page was returned successfully
        self.assertEqual(response.status_code,200)

    def test_signup_passwords_dont_match(self):
        response = self.test_client.post('/signup/',
                    {'username':'test','password1':'pass1234',
                    'password2':'p','email':'test@test.com'})

        # Assert that registration failed
        self.assertFalse(response.context['registerSuccess'])

        # Assert that passwords dont match
        self.assertTrue(response.context['passwordsDontMatch'])

        # Assert that the page was returned successfully
        self.assertEqual(response.status_code,200)

    def test_signup_username_missing(self):
        response = self.test_client.post('/signup/',
                    {'username':'','password1':'pass1234',
                    'password2':'pass1234','email':'test@test.com'})

        # Assert that registration failed
        self.assertFalse(response.context['registerSuccess'])

        # Assert that username is missing
        self.assertTrue(response.context['usernameMissing'])

        # Assert that the page was returned successfully
        self.assertEqual(response.status_code,200)

    def test_signup_password_missing(self):
        response = self.test_client.post('/signup/',
                    {'username':'test','password1':'',
                    'password2':'','email':'test@test.com'})

        # Assert that registration failed
        self.assertFalse(response.context['registerSuccess'])

        # Assert that password is missing
        self.assertTrue(response.context['passwordMissing'])

        # Assert that the page was returned successfully
        self.assertEqual(response.status_code,200)

    def test_signup_email_missing(self):
        response = self.test_client.post('/signup/',
                    {'username':'test','password1':'pass1234',
                    'password2':'pass1234','email':''})

        # Assert that registration failed
        self.assertFalse(response.context['registerSuccess'])

        # Assert that password is missing
        self.assertTrue(response.context['emailMissing'])

        # Assert that the page was returned successfully
        self.assertEqual(response.status_code,200)
