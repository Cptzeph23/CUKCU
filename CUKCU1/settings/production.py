import cukcu
from .base import *
import os

DEBUG = False

# Temporarily disable strict security settings until site is working later change to true
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000    # laater change to 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Render-specific fix
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'cukcu.onrender.com', '.onrender.com', 'www.cukcu.org', 'cukcu.org', 'https://cukcu.onrender.com', 'cukcu.onrender.com.']

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
