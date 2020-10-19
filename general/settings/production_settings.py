from general.settings.base_settings import *

ALLOWED_HOSTS = ['*']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.db(),
    }
}

# CACHES = {
#     # read os.environ['CACHE_URL'] and raises ImproperlyConfigured exception if not found
#     'default': env.cache(),
#     'redis': env.cache('REDIS_URL')
# }
