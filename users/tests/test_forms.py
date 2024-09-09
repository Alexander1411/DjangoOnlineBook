from django.test import TestCase
from users.forms import SignUpForm

class SignUpFormTest(TestCase):
    def test_form_valid(self):
        form = SignUpForm(data={
            'username': 'BookReader12',
            'email': '22bubnov@gmail.com',
            'password1': 'nicepassword12',
            'password2': 'nicepassword12',
            'phone_number': '0868745776',
            'city': 'Dublin',
            'birth_date': '31-08-1996'
        })
        self.assertTrue(form.is_valid())  # Assert that the form is valid with correct data

    def test_form_invalid(self):
        form = SignUpForm(data={
            'username': '',
            'email': 'best@email',
            'password1': 'bad',
            'password2': 'bad',
            'phone_number': '0005',
        })
        self.assertFalse(form.is_valid())  # Assert that the form is invalid with incorrect data

    def test_form_cleaned_data(self):
        form_data = {
            'username': 'BookReader10',
            'first_name': 'Alexander ',
            'last_name': 'Bubnov',
            'email': '22bubnov@gmail.com',
            'password1': 'GreatPassword4321!',
            'password2': 'GreatPassword4321!',
            'phone_number': '0868745776',
            'city': 'Dublin',
            'birth_date': '31-08-1996'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())  # Check if form is valid
        cleaned_data = form.cleaned_data
        self.assertEqual(cleaned_data['username'], 'BookReader10')
        self.assertEqual(cleaned_data['email'], '22bubnov@gmail.com')
        self.assertEqual(cleaned_data['phone_number'], '0868745776')
