

from pathlib import Path
import os

import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(BASE_DIR / '.env')


SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')



ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'phonenumber_field',

    'core',
    'invitation',
    'event',
    'event_gallery',
    'payment',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'template')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # `allauth`
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}




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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT=os.path.join(BASE_DIR,'static')
STATICFILES_DIRS=[
os.path.join(BASE_DIR,'project/static')
]

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = env('EMAIL_HOST_USER')    
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'home'


WHATSAPP_ACCESS_TOKEN = "EAARLBjv1kv4BP80ZBN2LsZAXNahxKl8Nh96UCkdIFqqBrfPj277vqZCYJtcuGoysZBqiL8Vne6tKhf74DfofBMbEZApHyzjWH2AvSnmlo9LH8g4Yk2GbbsKVwnZC5M4n2Cm5QxaKnfCokHzCceWdLiZCg6arMCmkfDxTrAKZA9ICnZAiTOIdW3nAaZAG4JGQggJWyrIqfCJzSOwS3Go9TZA3cEK5IzMesd5IQPQn98ED8uJS29DgrjaNcfHvS8zLgNOKAmtIPCLqCd9E8BLUe08FM7wua54BrGrP6r1XZB6R8pAZD"
WHATSAPP_PHONE_NUMBER_ID = "907716542416142"
WHATSAPP_API_URL = "https://graph.facebook.com/v22.0/"



# EMAIL_HOST_USER = 'follow.software.engineer@gmail.com'       
# EMAIL_HOST_PASSWORD = 'hhzs beiy rqiv ipay'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER