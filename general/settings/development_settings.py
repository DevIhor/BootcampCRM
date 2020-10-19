from general.settings.base_settings import *

ALLOWED_HOSTS = ['*']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / env('DATABASE_NAME'),
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'postgres',
    #     'USER': 'postgres',
    #     'HOST': 'db',
    #     'PORT': 5432,
    # }
}
