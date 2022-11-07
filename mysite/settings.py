"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from environs import Env # new (p-153)

env = Env() # new (p-153)
env.read_env() # new (p-153)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-spa!4(muo%a#hzen3v)^c@o@hhmfj&x0&y60!)-4$1xenczu)%'
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!

# DEBUG = True
DEBUG = env.bool("DJANGO_DEBUG") # new
# ALLOWED_HOSTS = []
ALLOWED_HOSTS = [".herokuapp.com", "localhost", "127.0.0.1"] # new (p-157)

# DEBUG = False # new (p-157)
# ALLOWED_HOSTS = [".herokuapp.com", "localhost", "127.0.0.1"] # new (p-157)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites", # new (p-132)
    # Third-party
    "crispy_forms", # new (p-125)
    "crispy_bootstrap5", # new (p-125)
    "allauth", # new (p-132)
    "allauth.account", # new (p-132)
    # Local
	"accounts.apps.AccountsConfig", # new
    "pages.apps.PagesConfig", # forgot to add it till now (p-125)
]

# django-allauth config (p-132)
LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT = "home" # new (p-135)
SITE_ID = 1 # new (p-132)
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend", # have no effect (p-132)
    "allauth.account.auth_backends.AuthenticationBackend", # new
)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend" # new (p-134)
ACCOUNT_SESSION_REMEMBER = True # new (p-139) [Removes Remember me]
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False # new (p-142)
# using allauth (p-16)
ACCOUNT_USERNAME_REQUIRED = False # new
ACCOUNT_AUTHENTICATION_METHOD = "email" # new
ACCOUNT_EMAIL_REQUIRED = True # new
ACCOUNT_UNIQUE_EMAIL = True # new

####

AUTH_USER_MODEL = "accounts.CustomUser" # new

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / "templates"], # new
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

"""
# After first build & run successfully
# replace this with the postgresql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
# (p-158) use environ
DATABASES = {
	"default": env.dj_db_url("DATABASE_URL",
	default="postgres://postgres@db/postgres")
}
"""
DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.postgresql",
		"NAME": "postgres",
		"USER": "postgres",
		"PASSWORD": "postgres",
		"HOST": "db",
		"PORT": 5432,
	}
}
"""

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"] # new
# before collectstatic for Production
STATIC_ROOT = BASE_DIR / "staticfiles" # new
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage" # new

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = "home" # new after login
LOGOUT_REDIRECT_URL = "home" # new

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5" # new (p-126)
CRISPY_TEMPLATE_PACK = "bootstrap5" # new (p-126)

