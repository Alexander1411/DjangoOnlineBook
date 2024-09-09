from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm # build in, handles creating a new user with a username and password
from .models import Profile
import logging

logger = logging.getLogger(__name__)

class SignUpForm(UserCreationForm): # main form used for new user registration, connects to the User (Pofile) model : https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/forms/
    email = forms.EmailField(required=True)  # allowing to check if the field is completed (email validation is kept because it directly concerns the User model and is a common practice to avoid duplicate emails)
    phone_number = forms.CharField(max_length=15, required=True) 
    city = forms.CharField(max_length=30, required=True)  # CharField A string field, for small- to large-sized strings
    birth_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type':'date'}), input_formats=['%Y-%m-%d', '%d-%m-%Y']) # date formats match how the date is entered by users. If users input dates in the format YYYY-MM-DD, then '%Y-%m-%d'

    class Meta:  # provides additional information about the Model class have created before. The metadata of the Model class is anything that is not a field :https://forum.djangoproject.com/t/adding-extra-fields-to-a-register-form/14922
        model = User # # This tells the form to use the User model
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2','phone_number', 'city', 'birth_date')

    def save(self, commit=True): # user information is saved to the database only after all the form fields are properly filled and validated
        user = super().save(commit=False) # part creates a new User object but doesn’t save it to the database just yet
        user.email = self.cleaned_data['email'] # sets the users email using the validated data from the form
        if commit: # if true it saves the user to the database and then updates the users profile with the additional data
            user.save()
            user.profile.phone_number = self.cleaned_data['phone_number'] # https://forum.djangoproject.com/t/django-model-form-not-taking-in-users/17846
            user.profile.city = self.cleaned_data['city']
            user.profile.birth_date = self.cleaned_data['birth_date']
            user.profile.save()
        return user

    ## This is a custom validation method to ensure the email address is unique 
    def clean_email(self): # retrieves the submitted email and checks if it already exists in the User model. If it does, it raises a validation error; YotubeTutorial / https://www.youtube.com/watch?v=1_c9fbvxNmo&t=3s
        email = self.cleaned_data.get('email') # gets the email entered by the user from the form data
        if User.objects.filter(email=email).exists(): # if email exists raise error. directly querying the User model to check if an email already exists in the database
            raise forms.ValidationError("Email already in use") 
        return email

# Form to update users basic information like first name, last name, and email, used when editing user details separately from the profile. in the User model.
class UserForm(forms.ModelForm): #updating basic User Information!!!!!!!!!!
    class Meta: 
        model = User
        fields = ['first_name', 'last_name', 'email']

#  part of my Profile model, extends the User model to hold additional information
class ProfileForm(forms.ModelForm):  # updating Profile Information!!!!!!!!!!!!!!!!!!!!!!!!!
    class Meta:
         model = Profile
         fields = ['phone_number','city','birth_date']

# Simple form to handle email notification preferences
class EmailNotificationForm(forms.Form):
    receive_notifications = forms.BooleanField(required=False)