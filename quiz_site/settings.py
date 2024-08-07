"""
Django settings for quiz_site project.

Generated by 'django-admin startproject' using Django 5.0.4
For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-0x00mwi)77h00ks0!u++nd503yrq_v1c_*dsqaf22@d8j%qa^v"

# SECiRITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "False") == "True"
print(f"DEBUG is set to {DEBUG}")
# This makes the DEBUG variable set dynamically depending on the environment.
# The local server should be set to True. The Heroku server should be set to False

#checks whether this instance is local or Production
IS_HEROKU_APP = "DYNO" in os.environ and not "CI" in os.environ

# On Heroku, it's safe to use a wildcard for `ALLOWED_HOSTS``, since the Heroku router performs
# validation of the Host header in the incoming HTTP request.
if IS_HEROKU_APP:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = [".localhost", "127.0.0.1", "[::1]", "0.0.0.0"]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]
# Application definition

INSTALLED_APPS = [
    #'quizes',
    "TestingApp",
    "quiztest",
    "rest_framework",
    "daphne",
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
    "userProfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

# Conditionally Sets up the Django Toolbar for debugging on the local server, and not on Heroku
if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]

    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]


ROOT_URLCONF = "quiz_site.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # 'DIRS': [],
        "DIRS": [str(BASE_DIR.joinpath("templates"))],  # new
        # 'DIRS': [os.path.join(BASE_DIR / 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # `allauth` needs this from django
                "django.template.context_processors.request",
            ],
        },
    },
]


WSGI_APPLICATION = "quiz_site.wsgi.application"

# This is for channels things
# May want to swap to REDIS_TLD_URL for full deployment
# Conditionally Sets up the which BackEnd for Channels Layers. Local:InMemory | Heroku:Redis
if DEBUG:
    # If DEBUG=TRUE, i.e., LOCAL
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        },
        "ROUTING": "userProfiles.routing.channel_routing",
    }

    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }
else:
    # If DEBUG=FALSE, i.e., PRODUCTION
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [os.environ.get("REDIS_URL", "redis://localhost:6379")]
            },
        },
        "ROUTING": "userProfiles.routing.channel_routing",
    }

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": [os.environ.get("REDIS_URL", "redis://localhost:6379")],
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "ssl_cert_reqs": None,
            },
        }
    }


ASGI_APPLICATION = "quiz_site.asgi.application"

SESSION_ENGINE = (
    "django.contrib.sessions.backends.cache"  # TEST 2 TO MAKE LOADING FASTER
)
SESSION_CACHE_ALIES = "default"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "d6f26nemgdgsoj",
        "USER": "ubjg99a8qcmm7o",
        "PASSWORD": "pe699a3bafb5874698abe70862bbefe5eb2437a608aa3ceb4cf801827d3c454b8",
        "HOST": "cb5ajfjosdpmil.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
        "PORT": "5432",
        "CONN_MAX_AGE": 60,  # TEST 1 TO MAKE LOADING FASTER
    }
}
#Force AllAuth to send requests through https
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
SOCIALACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

#verification settings for OAuth Apps:
SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "APP": {
            "client_id": "Ov23lit8Kp12dQZZsUqO",
            "secret": "c734357f06f6819081d035ff43a5f1fe2a13054e",
        },
        "VERIFIED_EMAIL": True,
    },
    "google": {
        "APP": {
            "client_id": "490286722574-423l5p2hc0hdfgmphe4gmlntqn89lcv6.apps.googleusercontent.com",
            "secret": "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",
        },
        "VERIFIED_EMAIL": True,
    },
}
#this allows the app to generate CSRF Tokens when deployed. Heroku blocks other heroku apps from generating our tokens.
CSRF_TRUSTED_ORIGINS =['https://*.herokuapp.com']

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = BASE_DIR / "productionfiles"

STATIC_URL = "/static/"

STATICFILES_DIRS = [BASE_DIR / "mystaticfiles"]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# allAuth Settings:
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_CONFIRM_EMAIL_ON_GET = False


# Idk if these additions work for rerouting
LOGIN_REDIRECT_URL = "/qSelect/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
