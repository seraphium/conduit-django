from conduit.settings.common import *
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': dj_database_url.config()
}

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True
