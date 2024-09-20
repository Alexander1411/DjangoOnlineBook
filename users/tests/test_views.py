from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Profile

class UserViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='LoveBooks4ever',
            password='gentlePassword77',
            email='22bubnov@gmail.com'
        )
        self.profile = Profile.objects.get(user=self.user)

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')

        # Test successful signup
        response = self.client.post(reverse('signup'), {
        'username': 'newLoveBooks4ever',
        'first_name': 'Alexander',
        'last_name': 'Bubnov',
        'email': 'new@bubnov.com',
        'password1': 'gentlePassword77',
        'password2': 'gentlePassword77',
        'phone_number': '0868745776',
        'city': 'Dublin',
        'birth_date': '1996-08-08'
    })
        if response.status_code != 302:
            print("Signup form errors:", response.context['form'].errors)
        else:
            print("Signup successful")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newLoveBooks4ever').exists())
        self.assertRedirects(response, reverse('home'))

        # Additional checks
        new_user = User.objects.get(username='newLoveBooks4ever')
        self.assertEqual(new_user.email, 'new@bubnov.com')
        self.assertEqual(new_user.first_name, 'Alexander')
        self.assertEqual(new_user.last_name, 'Bubnov')
    
        new_profile = Profile.objects.get(user=new_user)
        self.assertEqual(new_profile.phone_number, '0868745776')
        self.assertEqual(new_profile.city, 'Dublin')
        self.assertEqual(str(new_profile.birth_date), '1996-08-08')
        
    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

        # Test successful login
        response = self.client.post(reverse('login'), {
            'username': 'LoveBooks4ever',
            'password': 'gentlePassword77',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/home.html')
        self.assertIn('top_books', response.context)
        self.assertIn('recommended_books', response.context)

    def test_profile_view(self):
        self.client.login(username='LoveBooks4ever', password='gentlePassword77')
        response = self.client.get(reverse('view_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(response.context['object'], self.profile)

    #def test_edit_profile_view(self):
    #    self.client.login(username='LoveBooks4ever', password='gentlePassword77')
        
        # Test GET request
    #    response = self.client.get(reverse('edit_profile'))
    #    self.assertEqual(response.status_code, 200)
    #    self.assertTemplateUsed(response, 'users/profile_edit.html')

        # Test POST request for UserForm 
    #    response = self.client.post(reverse('edit_profile'),{
    #        'first_name': 'Alex',
    #        'last_name': 'Testing',
    #        'email': '22bubnov@gmail.com',
    #        'phone_number': '1234567890',
    #        'city': 'Berlin',
    #        'birth_date': '1995-01-01'
    #    })
        # Check if the form submission resulted in a redirect (successful submission)
    #    if response.status_code != 302:
    #        print("Form submission failed.")
    #        if 'user_form' in response.context:
    #            print("User form errors:", response.context['user_form'].errors)
    #        if 'profile_form' in response.context:
    #            print("Profile form errors:", response.context['profile_form'].errors)
    #    else:
    #        print("Form submission successful")#

    #    self.assertEqual(response.status_code, 302)
    #    self.assertRedirects(response, reverse('view_profile'))

        # Verifing profile update
    #    self.user.refresh_from_db()
    #    self.profile.refresh_from_db()
        #print(f"Updated email: {self.user.email}")
        #print(f"Updated first name: {self.user.first_name}")
        #print(f"Updated last name: {self.user.last_name}")
        #print(f"Updated phone number: {self.profile.phone_number}")
        #print(f"Updated city: {self.profile.city}")
        #print(f"Updated birth date: {self.profile.birth_date}")

     #   self.assertEqual(self.user.first_name, 'Alex')
      #  self.assertEqual(self.user.last_name, 'Testing')
       # self.assertEqual(self.user.email, '22bubnov@gmail.com')

        #self.assertEqual(self.profile.phone_number, '1234567890')
        #self.assertEqual(self.profile.city, 'Berlin')
        #self.assertEqual(str(self.profile.birth_date), '1995-01-01')
        

    def test_password_change_view(self):
        self.client.login(username='LoveBooks4ever', password='gentlePassword77')
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_change_form.html')

        # Test password change
        response = self.client.post(reverse('password_change'), {
            'old_password': 'gentlePassword77',
            'new_password1': 'newPassword123',
            'new_password2': 'newPassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('password_change_done'))