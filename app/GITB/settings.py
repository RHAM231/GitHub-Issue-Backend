import os
# from decouple import config
import json


with open('/etc/config.json') as config_file:
    config = json.load(config_file)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config['SECRET_KEY']

DEBUG = True

ALLOWED_HOSTS = ['*']

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_REFERRER_POLICY = 'same-origin'
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_HSTS_SECONDS = 2592000
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'sync.apps.SyncConfig',
    'base.apps.BaseConfig',
    'crispy_forms',
    'users.apps.UsersConfig',
    'issues.apps.IssuesConfig',
    'repositories.apps.RepositoriesConfig',
    'rest_framework',
    'consume_api.apps.ConsumeApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'GITB.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'base.context_processors.Master_Search_Form',
                'base.context_processors.get_profile',
            ],

            'libraries':{
                'filters': 'base.filters',
            }
        },
    },
]

WSGI_APPLICATION = 'GITB.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config.get('DB_NAME'),
#         'USER': config.get('DB_USER'),
#         'PASSWORD': config.get('DB_PASS'),
#         'HOST': config.get('DB_HOST'),
#         'PORT': '5432',
#     }
# }


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

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

# This may need tweeking
GH_TOKEN = config('GH_TOKEN')
GH_USER = config('GH_USER')

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ]
}


# CSP_DEFAULT_SRC = ["'none'"]
# CSP_SCRIPT_SRC = [
#     "https://stackpath.bootstrapcdn.com",
#     "https://cdn.jsdelivr.net",
#     "https://code.jquery.com",
#     "'self'"
# ]
# CSP_STYLE_SRC = [
#     "https://stackpath.bootstrapcdn.com",
#     "'self'"
# ]
# CSP_STYLE_SRC_ELEM = [
#     "https://use.fontawesome.com",
#     "https://fonts.googleapis.com",
#     "https://stackpath.bootstrapcdn.com",
#     "'self'"
# ]
# CSP_IMG_SRC = ["'self'"]
# CSP_MEDIA_SRC = ["'self'"]
# CSP_FRAME_SRC = ["'self'"]
# CSP_OBJECT_SRC = ["'self'"]
# CSP_FONT_SRC = [
#     "https://use.fontawesome.com",
#     "https://fonts.googleapis.com",
#     "https://fonts.gstatic.com/s/spinnaker/v12/w8gYH2oyX-I0_rvR6HmX1XYKmOo.woff2",
#     "https://fonts.gstatic.com/s/spinnaker/v12/w8gYH2oyX-I0_rvR6HmX23YK.woff2"
# ]