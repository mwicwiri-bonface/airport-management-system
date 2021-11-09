from core.settings.base import *

# Overriding settings
DEBUG = True

ALLOWED_HOSTS = ['airport.pythonanywhere.com']

# gmail smtp server config
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_SUBJECT_PREFIX = config('EMAIL_SUBJECT_PREFIX')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT')
