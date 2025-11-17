# coimpres_cuba/settings/production.py

from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tu_usuario$nombrebase',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'tu_usuario.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
