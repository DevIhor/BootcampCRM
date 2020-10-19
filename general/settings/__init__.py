"""
Django settings for BootcampCRM project.
"""
import environ

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()

DEBUG = env('DEBUG')

if DEBUG:
    from general.settings.development_settings import *
else:
    from general.settings.production_settings import *
