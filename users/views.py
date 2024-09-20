import re
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .forms import SignUpForm, UserForm, ProfileForm  # Consolidated imports
from .models import Profile  # Consolidated imports
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.views import LoginView, LogoutView  # Import built-in views
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from books.models import Catalog  # Import the Catalog model from the books app
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
import logging
import random


# Set up logging to capture events, which is useful for debugging and tracking application behaviour
logger = logging.getLogger(__name__)

# Sign Up View (Class-Based), Uses Django's FormView to handle form submission, validation, and saving
class SignUpView(FormView): # SignUpForm connected to forms
    template_name = 'users/signup.html'
    form_class = SignUpForm  # Im telling Django to use the custom form class SignUpForm to render the form, handle validation, and process the data
    success_url = reverse_lazy('home') # reverse_lazy waits until the right moment to get the URL, preventing errors during startup : https://stackoverflow.com/questions/31275574/reverse-for-success-url-on-django-class-based-view-complain-about-circular-impor

    def form_valid(self, form): # if all the input data is correct (built-in methods)
            user = form.save()
            login(self.request, user)
            messages.success(self.request, "Your account was created successfully")
            return super().form_valid(form) # super() avoids repeating code, Django to handle valid/invalid form
            

    def form_invalid(self, form): # built-in methods provided by Django in the FormView class: automatically called
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field.replace('_', ' ').capitalize()}: {error}") # testing this 
            return super().form_invalid(form)
    
# Custom validation for phone number and invite code, the phone number matches an international format using a regular expression
def validate_phone_number(phone_number):
    if not re.match(r'^(08[3-9]\d{7})|(0[1-9]\d{8})$', phone_number):
        raise ValidationError("Enter a valid Irish phone number.")
    
# Login 
class CustomLoginView(LoginView):
    template_name = 'registration/login.html' 
    # I switched from a function to Djangos builtin LoginView class to simplify the code and let Django handle the login process automatically, making it easier to manage and maintain.

# Home page. This is a simple view that renders the homepage template // https://stackoverflow.com/questions/73177899/django-templateview-not-recognizing-my-template-name
class HomeView(TemplateView): #HomeView is my custom class, TemplateView is my parent class
    template_name = 'users/home.html'  # I switched from using a function to a class because Djangos classbased views make the code cleaner, more reusable, and easier to expand.

    def get_context_data(self, **kwargs): # (I override it) method is overridden to add custom data: https://medium.com/@hassanraza/when-to-use-get-get-queryset-get-context-data-in-django-952df6be036a#:~:text=get_context_data(),to%20display%20in%20your%20templates.
        context = super().get_context_data(**kwargs) ##Django gives default data sent to template: https://docs.djangoproject.com/en/5.1/topics/class-based-views/generic-display/
        all_books = list(Catalog.objects.all())  # fetches a list of data from database 
        
        num_books = min(20, len(all_books)) # Veriable, all of my books from my inventory 
        
        top_books = random.sample(all_books, num_books) # random method to sample books : https://www.geeksforgeeks.org/python-random-sample-function/
        recommended_books = random.sample(all_books, num_books)
        
        # Ive slides the sample books into two 
        context['top_books'] = [top_books[i:i + 5] for i in range(0, len(top_books), 5)] # grouped books into 5s for easier display of carusel 
        context['recommended_books'] = [recommended_books[i:i + 5] for i in range(0, len(recommended_books), 5)]
        
        return context

# View Profile (User must be logged in) : https://www.reddit.com/r/django/comments/l2jxe3/hello_i_need_help_with_detailview_i_have_written/
class ProfileView(LoginRequiredMixin, DetailView): # LoginRequiredMixin is a mixin that ensures the user must be logged in 
    model = Profile # automatically query this model to retrieve the required object
    template_name = 'users/profile.html' # does as it says really 

    def get_object(self): # retrieve the object that the view will display, Im overriding it to ensure that the Profile shown is the one linked to the currently logged-in use
        # Ensures it fetches the profile of the currently loggedin user
        return Profile.objects.get(user=self.request.user) # performs a query to find the Profile associated with the current user, and this profile object will be passed to the template.

# Allows users to edit their profile information, handles updating both the User model and the Profile model.
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile  # We are editing the Profile model
    template_name = 'users/profile_edit.html'
    form_class = ProfileForm  # This is for Profile model fields (phone number, city, birth date)
    second_form_class = UserForm  # This is for User model fields (first name, last name, email)

    def get_object(self):
        # Fetch the Profile object associated with the logged-in user
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = self.second_form_class(instance=self.request.user)  # Pre-fill UserForm with current user data
        context['profile_form'] = self.form_class(instance=self.get_object())  # Pre-fill ProfileForm with current profile data
        return context

    def post(self, request, *args, **kwargs):
        user_form = self.second_form_class(request.POST, instance=request.user)
        profile_form = self.form_class(request.POST, instance=self.get_object())

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Save user data (first name, last name, email)
            profile_form.save()  # Save profile data (phone number, city, birth date)
            messages.success(request, 'Profile updated successfully!')
            return redirect('view_profile')
        else:
            return self.render_to_response(self.get_context_data(user_form=user_form, profile_form=profile_form))

class MyPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_message = "Your password was changed successfully."
    success_url = reverse_lazy('password_change_done')
    

# endpoint books/
def books_list_view(request):
    return render(request, 'books/books_list.html')


from django.shortcuts import render

def test_view(request):
    return render(request, 'test.html')
