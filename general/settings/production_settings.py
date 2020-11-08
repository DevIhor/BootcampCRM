from general.settings.base_settings import *

# Database
DATABASES = {
    'default': {
        'ENGINE': env('SQL_ENGINE', default='django.db.backends.postgresql'),
        'NAME': env('SQL_DATABASE', default='postgresql'),
        'USER': env('SQL_USER', default='user'),
        'PASSWORD': env('SQL_PASSWORD', default='password'),
        'HOST': env('SQL_HOST', default='localhost'),
        'PORT': env('SQL_PORT', default='5432'),
    }
}

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env('EMAIL_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD')
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# CACHES = {
#     # read os.environ['CACHE_URL'] and raises ImproperlyConfigured exception if not found
#     'default': env.cache(),
#     'redis': env.cache('REDIS_URL')
# }
