from django import forms

class CheckoutForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=255)
    country = forms.ChoiceField(choices=[('IE', 'Ireland')])  # Add more countries for future
    stripeToken = forms.CharField(widget=forms.HiddenInput(), required=False)