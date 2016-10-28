from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .models import Event, Interest, UserProfile, Location, Interest

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

class MapTestCase(TestCase):
    test_client = None
    interests = None

    def setUp(self):
        self.test_client = Client()
        self.test_client.post('/signup/',
                    {'username':'test','password1':'pass1234',
                    'password2':'pass1234','email':'test@test.com'})
        self.test_client.post('/',
                    {'username':'test', 'password':'pass1234'})

    def test_get_map_success(self):
        response = self.test_client.get('/map/')

        # Assert that the page was loaded correctly
        self.assertEqual(response.status_code,200)

class GetUserDetailsTestCase(TestCase):
    test_client = None
    interests = None

    def setUp(self):
        self.test_client = Client()
        self.test_client.post('/signup/',
                    {'username':'test','password1':'pass1234',
                    'password2':'pass1234','email':'test@test.com'})
        self.test_client.post('/',
                    {'username':'test', 'password':'pass1234'})

    def test_get_user_details_success(self):
        response = self.test_client.get('/get_user_details/')

        # Assert that the data was correctly retreived
        self.assertEqual(response.json()['username'],'test')

        # Assert that the response JSON was received correctly
        self.assertEqual(response.status_code,200)

    def test_get_user_details_failed(self):
        response = self.test_client.post('/get_user_details/', {})

        # Assert that error 405 was thrown because this endpoint only
        # accepts a GET request
        self.assertEqual(response.status_code,405)

class GetEventTestCase(TestCase):
    test_client = None

    def setUp(self):
        self.test_client = Client()
        self.test_client.post('/signup/',
                    {'username':'test','password1':'pass1234',
                    'password2':'pass1234','email':'test@test.com'})
        self.test_client.post('/',
                    {'username':'test', 'password':'pass1234'})
        interests = Interest(interest_name='test')
        interests.save()
        profile = UserProfile.objects.get(username='test')
        location = Location(street_number=1234,street_name='street_name',
            suburb='suburb',city='city',zipcode=2000,latitude=30,
            longitude=30)
        location.save()
        meet = Event(name='test',from_time='2016-10-22',to_time='2016-10-22',
            description='description',is_private=False,
            location=location,creator=profile)
        meet.save()
        meet.interests = [interests]
        meet.save()

    def test_get_events_success(self):
        response = self.test_client.post('/get_events/',
                                        {'interests':['test']})

        # Assert that events were returned
        self.assertIsNotNone(response.json()['events'])

        # Assert that the response JSON was received correctly
        self.assertEqual(response.status_code,200)

    def test_get_events_failed(self):
        response = self.test_client.get('/get_events/')

        # Assert that error 405 was thrown because this endpoint only
        # accepts a POST request
        self.assertEqual(response.status_code,405)

class GoingToEventTestCase(TestCase):
    test_client = None
    event_id = None
    profile = None
    meet = None

    def setUp(self):
        self.test_client = Client()
        self.test_client.post('/signup/',
                    {'username':'test','password1':'pass1234',
                    'password2':'pass1234','email':'test@test.com'})
        self.test_client.post('/',
                    {'username':'test', 'password':'pass1234'})
        interests = Interest(interest_name='test')
        interests.save()
        self.profile = UserProfile.objects.get(username='test')
        location = Location(street_number=1234,street_name='street_name',
            suburb='suburb',city='city',zipcode=2000,latitude=30,
            longitude=30)
        location.save()
        self.meet = Event(name='test',from_time='2016-10-22',to_time='2016-10-22',
            description='description',is_private=False,
            location=location,creator=self.profile)
        self.meet.save()
        self.meet.interests = [interests]
        self.meet.save()
        self.event_id = self.meet.pk

    def test_going_to_event_success(self):
        response = self.test_client.post('/going_to_event/',
                                        {'event_id':self.event_id})

        # Assert that the user is now going to the event
        events = Event.objects.filter(creator=self.profile)
        self.assertIn(self.meet, events)

        # Assert that the response JSON was received correctly
        self.assertEqual(response.status_code,200)

    def test_going_to_event_get_failed(self):
        response = self.test_client.get('/going_to_event/')

        # Assert that error 405 was thrown because this endpoint only
        # accepts a POST request
        self.assertEqual(response.status_code,405)

class DeleteEventTestCase(TestCase):
    test_client = None
    event_id = None
    profile = None
    meet = None

    def setUp(self):
        self.test_client = Client()
        self.test_client.post('/signup/',
                    {'username':'test','password1':'pass1234',
                    'password2':'pass1234','email':'test@test.com'})
        self.test_client.post('/',
                    {'username':'test', 'password':'pass1234'})
        interests = Interest(interest_name='test')
        interests.save()
        self.profile = UserProfile.objects.get(username='test')
        location = Location(street_number=1234,street_name='street_name',
            suburb='suburb',city='city',zipcode=2000,latitude=30,
            longitude=30)
        location.save()
        self.meet = Event(name='test',from_time='2016-10-22',to_time='2016-10-22',
            description='description',is_private=False,
            location=location,creator=self.profile)
        self.meet.save()
        self.meet.interests = [interests]
        self.meet.save()
        self.event_id = self.meet.pk

    def test_going_to_event_success(self):
        response = self.test_client.post('/delete_event/',
                                        {'event_id':self.event_id})

        # Assert that meet no longer exists
        events = Event.objects.all()
        self.assertNotIn(self.meet, events)

        # Assert that the response JSON was received correctly
        self.assertEqual(response.status_code,200)

    def test_going_to_event_get_failed(self):
        response = self.test_client.get('/delete_event/')

        # Assert that error 405 was thrown because this endpoint only
        # accepts a POST request
        self.assertEqual(response.status_code,405)
