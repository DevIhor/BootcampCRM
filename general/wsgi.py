"""
WSGI config for BootcampCRM project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'general.settings')
application = get_wsgi_application()
