from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='LoveBooks4ever',
            password='gentlePassword77'
        )

    # Testing Sign Up form views
    def test_view(self):
        response = self.client.get(reverse('signup')) # reverse used to generate URLs by their name, avoiding hardcoding URL # https://medium.com/@buczynski.rafal/nawigacja-przez-django-testowanie-adres%C3%B3w-url-77b05cb30d87#:~:text=URL%20testing%20basics%20in%20Django&text=The%20'reverse'%20function%20allows%20you,but%20also%20easier%20to%20manage.
        self.assertEqual(response.status_code, 200)  # Check that the signup page loads correctly /Setting the language: https://docs.djangoproject.com/en/5.1/topics/testing/tools/
        self.assertTemplateUsed(response, 'users/signup.html')  # Ensure correct template is used

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)  # Ensure the login page loads correctly
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_profile_view(self):
        self.client.login(username='LoveBooks4ever', password='gentlePassword77')  # Login the test user
        response = self.client.get(reverse('view_profile'))
        self.assertEqual(response.status_code, 200)  # Ensure the profile page loads correctly
        self.assertTemplateUsed(response, 'users/profile.html')  # Check the correct template
