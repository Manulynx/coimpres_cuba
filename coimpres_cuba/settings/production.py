# coimpres_cuba/settings/production.py

from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Coimpre$default',
        'USER': 'Coimpre',
        'PASSWORD': 'Manuel.980317',
        'HOST': 'Coimpre.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
