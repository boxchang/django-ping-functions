from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vvf3s8tgg#p^xlfta#cu3g)j5^0h@onjpt6!%9ku7f2mg53dha'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}