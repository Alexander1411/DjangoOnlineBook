import os
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Always first. On top.
BASE_DIR = Path(__file__).resolve().parent.parent


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',  # Using FileHandler without maxBytes and backupCount
            'filename': os.path.join(BASE_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',  # Changed level to INFO
            'propagate': True,
        },
    },
}


LOGIN_REDIRECT_URL = 'home'  # Redirect after login
LOGOUT_REDIRECT_URL = 'home'  # Redirect after logout
LOGIN_URL = 'login'  # The view name to redirect when login is required
LOGOUT_URL = 'logout'  # The view name to log out

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7l8xkk8e@miorptk=6^vd6gic1fclu(!3$c@e)lc2(@kr35t_d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ASGI_APPLICATION = 'onlinebooks.asgi.application'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'books',
    'orders',
    'users.apps.UsersConfig',  # Instead of just users
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'onlinebooks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # This way, Django will look in both directories for templates
        'DIRS': [BASE_DIR / 'users' / 'templates' / 'users',
],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'onlinebooks.wsgi.application'
DATE_INPUT_FORMATS = ['%d-%m-%Y']


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'onlinebooks_db',
        #'NAME': 'test_onlinebooks_db',
        'USER': 'onlinebooks_user',
        'PASSWORD': 'alexander',  
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles_collected'
STATICFILES_DIRS = [
    BASE_DIR / "users/static",
]


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
#MAIL_HOST_USER = '22bubnov@gmail.com'
#EMAIL_HOST_PASSWORD = 'alexander'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For testing


STRIPE_PUBLIC_KEY = 'pk_test_51PwR3zQ74VVZ9ijxqV4Ecic3xB6HGGxcTu6fTupedTIaZEwKQfcqMOAIiUkQE03oT00cDrXY5Uc9QgnvRi5MS4JL00axL3T4gd' # https://dashboard.stripe.com/test/dashboard
STRIPE_SECRET_KEY = 'sk_test_51PwR3zQ74VVZ9ijxjNfe9MIl5dgH2Uo6TPhbl5Ci6CPY7EIPXrfgWdXZJr068QPtTkoni93bQuT5trjcYtj04hUf00NOxrMfu9'
