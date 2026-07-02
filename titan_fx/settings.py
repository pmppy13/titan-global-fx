import os
import dj_database_url
from pathlib import Path
from decouple import config

# ============================================================
# BASE DIRECTORY
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# SECURITY - Using Environment Variables
# ============================================================
SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-change-this-in-production')

# ============================================================
# DEBUG - True for demo, False for production
# ============================================================
DEBUG = config('DEBUG', default=False, cast=bool)

# ============================================================
# ALLOWED HOSTS - Allow all for demo
# ============================================================
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')

# ============================================================
# APPLICATION DEFINITION
# ============================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'whitenoise.runserver_nostatic',
    'accounts',
    'core',
    'dashboard',
    'transactions',
    'admin_dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'titan_fx.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'titan_fx.wsgi.application'

# ============================================================
# DATABASE - PostgreSQL on Render
# ============================================================
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ============================================================
# PASSWORD VALIDATION
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================================
# INTERNATIONALIZATION
# ============================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True

# ============================================================
# STATIC & MEDIA FILES
# ============================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Whitenoise for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================
# CUSTOM USER MODEL
# ============================================================
AUTH_USER_MODEL = 'accounts.User'

# ============================================================
# AUTHENTICATION URLS
# ============================================================
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:login_redirect'
LOGOUT_REDIRECT_URL = 'core:home'

# ============================================================
# CRISPY FORMS
# ============================================================
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ============================================================
# RENDER-SPECIFIC: Allow admin access from any IP (Demo Only)
# ============================================================
INTERNAL_IPS = ['*']

# ============================================================
# SECURITY - Relaxed for demo on Render free tier
# ============================================================
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)

# ============================================================
# LOGGING (Optional - for debugging on Render)
# ============================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}