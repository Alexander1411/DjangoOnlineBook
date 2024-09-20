from django import forms

class StripePaymentForm(forms.Form):
    stripeToken = forms.CharField()
