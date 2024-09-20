from django.test import TestCase
from orders.forms import StripePaymentForm

class StripePaymentFormTests(TestCase):
    def test_valid_stripe_payment_form(self):
        form = StripePaymentForm(data={'stripeToken': 'valid_token'})
        self.assertTrue(form.is_valid())

    def test_invalid_stripe_payment_form(self):
        form = StripePaymentForm(data={'stripeToken': ''})
        self.assertFalse(form.is_valid())
