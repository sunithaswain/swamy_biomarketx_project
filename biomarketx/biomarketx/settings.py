"""
Django settings for biomarketx project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ye#!wi9q=gvnu(bd24v@k3yrl8sc6_*cf)b*9izh_6qn#k#*c#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_ID = 1

ALLOWED_HOSTS = []

TEMPLATE_DEBUG = DEBUG

notification = "notification"

AUTH_USER_MODEL = 'auth.User'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django.contrib.sites',
    'allauth',
    'allauth.socialaccount',
    'allauth.account',
    'biomarketxapp',
    'bootstrapform',
    'ckeditor',
    'ckeditor_uploader',
    #'demo_application',
    'widget_tweaks',
    'pagination',
    'backend',
    'aloha_editor',
    'django_wysiwyg',
    'stripe',
    'cities_light'
    # 'django_messages',

]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'pagination.middleware.PaginationMiddleware',
]

ROOT_URLCONF = 'biomarketx.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'django.core.context_processors.media',
                
                'django.core.context_processors.request',
                # 'django_messages.context_processors.inbox',
                # "staticfiles.context_processors.static",
            ],
        },
    },
]


WSGI_APPLICATION = 'biomarketx.wsgi.application'

BOOTSTRAP_ADMIN_SIDEBAR_MENU = True

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# } 

DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'FinalBiomarketx',
                'USER': 'biomarketx',
                'PASSWORD': 'biomarketx',
                'HOST': 'localhost',
                'PORT': '3306',
                
            }
        }



DJANGO_WYSIWYG_FLAVOR = "ckeditor"
CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en']
CITIES_LIGHT_INCLUDE_COUNTRIES = ['US']
CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC', 'PPLF', 'PPLG', 'PPLL', 'PPLR', 'PPLS', 'STLMT',]

# DATABASES = {
#             'default': {
#                 'ENGINE': 'django.db.backends.mysql',
#                 'NAME': 'biomarketxnew',
#                 'USER': 'biomarketx',
#                 'PASSWORD': 'biomarketx',
#                 'HOST': 'localhost',
#                 'PORT': '3306',
                
#             }
#         }

# TEMPLATE_CONTEXT_PROCESSORS = (   
#     # Required by `allauth` template tags
#     'django.core.context_processors.request',
  
#     # `allauth` specific context processors
#     # 'allauth.account.context_processors.account',
#     # 'allauth.socialaccount.context_processors.socialaccount',
    
# )

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGIN_URL='/login/'

# LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'

# AUTHENTICATION_BACKENDS = (
#     'biomarketxapp.backends.EmailBackend',
#     'django.contrib.auth.backends.ModelBackend'
#     )

AUTHENTICATION_BACKENDS = (
    'biomarketxapp.backends.EmailBackend',
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_AUTHENTICATION_METHOD = 'email'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True  
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587  
EMAIL_HOST_USER = 'vinodsesetti@gmail.com'  
EMAIL_HOST_PASSWORD = '8801757981'

STATIC_URL = '/static/'

STATIC_ROOT = '%sstatic/' % BASE_DIR
# MEDIA_URL = '/static/media/'
# MEDIA_ROOT = '%sstatic/media/' % BASE_DIR

# MEDIA_URL = '/media/'
# MEDIA_ROOT = '%s/media/' % BASE_DIR
# MEDIA_ROOT = os.path.join(BASE_DIR, '/media/')
# # MEDIA_URL = '/media/'
# MEDIA_URL = '/media/'

TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.load_template_source",
    "django.template.loaders.app_directories.load_template_source",
]


MEDIA_ROOT = os.path.join(BASE_DIR, "static/media")
MEDIA_URL = 'static/media/'
# allauth.account.signals.user_logged_in(request, user)
# allauth.account.signals.user_signed_up(request, user)
print "$$$$$$$$$$$$$$$"
print MEDIA_ROOT

# upload_to = MEDIA_ROOT

# upload_to = MEDIA_URL

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "media"),)

CKEDITOR_UPLOAD_PATH = "uploads/"

    # CKEDITOR_CONFIGS = {
    #     'awesome_ckeditor': {
    #         'toolbar': 'Basic',
    #     },
    # }
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'



#stripe stuff
#stripe Test keys

STRIPE_PUBLISHABLE_KEY="pk_test_TSCO6ZbV5l1MkJY6xmp4T0iW"

STRIPE_SECRET_KEY="sk_test_gYOUiG8YJv9hPdDTBhbZ1qxb"


#Live keys

# STRIPE_PUBLISHABLE_KEY="pk_live_v2TBaVeirxVByMfmtj4FdmTA"

# STRIPE_SECRET_KEY="sk_live_F97RNSmCm2NHtd46pPHYyiCh"

