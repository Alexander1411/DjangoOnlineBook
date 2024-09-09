from django.test import TestCase
from books.forms import CheckoutForm

class CheckoutFormTest(TestCase):
    def test_valid_data(self): # checking if the form is valid
        form_data = {
            'address': '123 Fake Street',
            'city': 'Dublin',
            'zip_code': 'D16 H11NN',
            'payment_method': 'stripe',
        }
        form = CheckoutForm(data=form_data)
        self.assertTrue(form.is_valid())  # True if valid with correct data

    def test_missing_data(self): # testing with missing field 
        form_data = {
            'address': '', # empty field here
            'city': 'Dublin',
            'zip_code': 'D01',
            'payment_method': 'stripe',
        }
        form = CheckoutForm(data=form_data)
        self.assertFalse(form.is_valid())  # False if invalid when field is missing

    def test_invalid_zip(self): # Testing to see if the form still valid with wrong/incoplete zip code
        form_data = {
            'address': '123 Fake Street',
            'city': 'Dublin',
            'zip_code': '',  # Missing zip code
            'payment_method': 'credit',
        }
        form = CheckoutForm(data=form_data)
        self.assertFalse(form.is_valid())  # False if invalid with a wrong zip code
