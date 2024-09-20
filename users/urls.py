from django.urls import path
from django.views.generic import TemplateView
from .views import SignUpView, CustomLoginView, ProfileView, EditProfileView, HomeView, MyPasswordChangeView
from django.contrib.auth.views import LogoutView  # Import the correct LogoutView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Use the HomeView class instead of directly using TemplateView
    path('signup/', SignUpView.as_view(), name='signup'),  # Use SignUpView.as_view() for sign-up
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='view_profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('2fa/', TemplateView.as_view(template_name='users/two_factor_authentication.html'), name='two_factor_authentication'),
    path('logout/', LogoutView.as_view(), name='logout'),  
    path('books/', views.books_list_view, name='books'),
    

    # Password reset URLs
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('test/', views.test_view, name='test'),
]

