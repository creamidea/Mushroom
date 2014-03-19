from os.path import dirname, join, abspath
__dir__ = dirname(abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sqlite.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}
# DATABASE_ENGINE = 'django.db.backends.sqlite3'
# DATABASE_NAME = 'gevent-webchat.sqlite'
# DATABASE_USER = ''
# DATABASE_PASSWORD = ''
# DATABASE_HOST = ''
# DATABASE_PORT = ''
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = join(__dir__, 'static')
MEDIA_URL = '/static/media/'
SECRET_KEY = 'nv8(yg*&1-lon-8i-3jcs0y!01+rem*54051^5xt#^tzujdj!c'
TEMPLATE_LOADERS = (
    # 'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.filesystem.Loader',
    # 'django.template.loaders.app_directories.load_template_source',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
)
ROOT_URLCONF = 'webchat.urls'
TEMPLATE_DIRS = (
    join(__dir__, 'templates')
)
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
)
