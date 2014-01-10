# -*- coding: utf-8 -*-

# Django settings for NodeSite project.
import os

DEBUG = True
# DEBUG = False
TEMPLATE_DEBUG = DEBUG
PROJECT_NAME = 'NodeSite'

MIDDLEWARE_PORT = 10002
MIDDLEWARE_ADDRESS = "192.168.1.250"

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sqlite3.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

CACHES = {
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    #     # 'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    #     }
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '10.18.32.80:11211',
    }
}
    
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['127.0.0.1']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
# TIME_ZONE = 'America/Chicago'
TIME_ZONE = 'Asia/Shanghia'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-CN'
# LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
# STATIC_ROOT = 'F:/WSNG/Mushroom/NodeSite/static/'
# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_ROOT = './static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'static').replace('\\','/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'pku##pd3@23vrzutuizippc(-zt5^$c)xc*%pq!i2-=494mf=j'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = '%s.urls' % PROJECT_NAME

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = '%s.wsgi.application' % PROJECT_NAME

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
     os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    
    # 账户管理 
    '%s.accounts' % PROJECT_NAME,
    # 系统设置
    '%s.mushroom' % PROJECT_NAME,
    
)
    
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# TEMPLATE_CONTEXT_PROCESSORS = (
#     # 'django.core.context_processors.request',
#     # 'django.core.context_processors.auth',
#     # 'django.core.context_processors.debug',
#     # 'django.core.context_processors.i18n',
#     # 'django.core.context_processors.media',
# )

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# ===============================================
# Mail Server
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True 
# ==============================================

# ===============================================
# pipeline settings
# 将pipeline融入django
INSTALLED_APPS += (
    # django开发工具，
    # 用于coffee->js
    # compressor
    'pipeline',
)
MIDDLEWARE_CLASSES += (
    # Compressor
    'django.middleware.gzip.GZipMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
)
PIPELINE = True
# 使用的存储方式
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# 在windows下开发，需要加入这句，否则将会报错：
# CompressorError: The system cannot find the path specified.
# 这个应该是路径配置问题，在Windows上的路径配置实在太让人纠结了。
PIPELINE_YUGLIFY_BINARY = 'yuglify'

# 因为实在Windows上开发，所以默认的coffee,lessc不能使用，需要手动更改
PIPELINE_COFFEE_SCRIPT_BINARY = 'coffee'
PIPELINE_COFFEE_SCRIPT_ARGUMENTS = '-bc'
PIPELINE_LESS_BINARY = 'lessc'
PIPELINE_LESS_ARGUMENTS = '-x'
# 还没有想好如何配置yui-compressor压缩
# PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'
# PIPELINE_CSS_COMPRESSOR = None
# JS压缩貌似有问题，会报错在windows:CompressorError: The system cannot find the path specified.
PIPELINE_JS_COMPRESSOR = None
# 配置编译器，参数在上面
PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
    'pipeline.compilers.coffee.CoffeeScriptCompiler',
)

# 这里是写css文件，less文件会被自动编译
PIPELINE_CSS = {
    'bootstrap': {
        'source_filenames': (
            'vendor/css/bootstrap.min.css',
            'vendor/css/bootstrap-theme.min.css',
        ),
        'output_filename': 'css/bootstrap.css',
    },
    'normalize': {
        'source_filenames': (
            'vendor/css/normalize.css',
        ),
        'output_filename': 'css/normalize.css',
    },
    'main': {
        'source_filenames': (
            'less/login.less',
            'less/echo.less',
            'less/main.less',
            'vendor/css/main.css',
        ),
        'output_filename': 'css/main.css',
    },
    'le': {
        'source_filenames': (
            'less/le.less',
        ),
        'output_filename': 'css/le.css',
    },
}

# 这里就是写js文件，coffee文件会被自动编译
PIPELINE_JS = {
    'jquery': {
        'source_filenames': (
            'vendor/js/jquery-1.10.2.min.js',
        ),
        'output_filename': 'js/jquery.min.js',
    },
    'handlebars': {
        'source_filenames': (
            'vendor/js/handlebars-v1.1.2.js',
        ),
        'output_filename': 'js/handlebars.min.js',
    },
    'underscore': {
        'source_filenames': (
            'vendor/js/underscore-min.js',
        ),
        'output_filename': 'js/underscore-min.js',
    },
    'bootstrap': {
        'source_filenames': (
            'vendor/js/bootstrap.min.js',
        ),
        'output_filename': 'js/bootstrap.min.js',
    },
    'modernizr': {
        'source_filenames': (
            'vendor/js/modernizr-2.6.2.min.js',
        ),
        'output_filename': 'js/modernizr.min.js',
    },
    # -----------------------------------------
    'plugins': {
        'source_filenames': (
            'coffee/plugins.coffee',
        ),
        'output_filename': 'js/plugins.js',
    },
    'main': {
        'source_filenames': (
            'coffee/main.coffee',
        ),
        'output_filename': 'js/main.js',
    },
    'components': {
        'source_filenames': (
            'coffee/login.coffee',
            'coffee/room.coffee',
            'coffee/sidebar.coffee',
            'coffee/setting.coffee',
        ),
        'output_filename': 'js/components.js',
    },
}
# =============================================================
