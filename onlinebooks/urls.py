from django.contrib import admin
from django.urls import path, include
from users.views import SignUpView, CustomLoginView, ProfileView, EditProfileView, HomeView  # Updated imports for CBVs
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),  # Use HomeView for the home page
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Corrected reference to CustomLoginView
    path('profile/', ProfileView.as_view(), name='view_profile'),  # Corrected reference to ProfileView
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),  # Corrected reference to EditProfileView
    path('books/', include('books.urls')),  # Includes the books' URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Built-in Django auth views
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('users/', include('users.urls')),
    path('', include('users.urls')),  # Directs root URL to users.urls
    path('books/', include('books.urls')),  # Includes the books' URLs

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    
