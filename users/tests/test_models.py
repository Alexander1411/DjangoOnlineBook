from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='BookReader12',
            password='goodpassword12'
        )
        self.profile = Profile.objects.get(user=self.user)  # Access the automatically created profile

    def test_prof_creation(self):
        self.assertEqual(self.user.username, 'BookReader12')
        self.assertTrue(hasattr(self.user, 'profile'))  # Check that the user has a profile
        self.assertEqual(self.profile.user, self.user)  # Ensure that profile belongs to the correct user
