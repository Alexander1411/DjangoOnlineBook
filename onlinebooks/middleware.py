from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class AdminSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            # Use a different session engine for the admin
            settings.SESSION_COOKIE_NAME = 'admin_sessionid'
            settings.SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Default session engine
        else:
            # Use the normal session for the rest of the site
            settings.SESSION_COOKIE_NAME = 'website_sessionid'
            settings.SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'  # Cached DB session
