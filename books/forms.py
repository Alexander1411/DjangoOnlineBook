from django import forms

class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=20)
    payment_method = forms.ChoiceField(choices=[('credit', 'Debit Card'), ('stripe', 'Stripe')])
