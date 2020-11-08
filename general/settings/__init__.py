"""
Django settings for BootcampCRM project.
"""
import environ

from dotenv import load_dotenv
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(PROJECT_DIR / 'env/.env')

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()

DEBUG = env('DEBUG')

if DEBUG:
    from general.settings.development_settings import *
else:
    from general.settings.production_settings import *
