from general.settings.base_settings import *

# Database
DATABASES = {
    'default': {
        'ENGINE': env('SQL_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': env('SQL_DATABASE', default='db.sqlite3'),
        'USER': env('SQL_USER', default='user'),
        'PASSWORD': env('SQL_PASSWORD', default='password'),
        'HOST': env('SQL_HOST', default='localhost'),
        'PORT': env('SQL_PORT', default='5432'),
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
