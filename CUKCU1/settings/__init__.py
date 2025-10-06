import os

# Default to using the base settings
from .base import *

# Use production settings if DJANGO_SETTINGS_MODULE is set to production
if os.environ.get('DJANGO_SETTINGS_MODULE') == 'CUKCU1.settings.production':
    from .production import *