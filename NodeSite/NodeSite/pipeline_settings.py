# -*- coding: utf-8 -*-
from django_settings import *

# ============================================================
# pipeline
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
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_CSS = {
    'styles': {
        'source_filenames': (
            'css/normalize.css',
            'css/main.css',
        ),
        'output_filename': 'css/styles.css',
    },
    'le': {
        'source_filenames': (
            'css/le.less',
        ),
        'output_filename': 'css/le.css',
    },
}

PIPELINE_JS = {
    'test': {
        'source_filenames': (
            'js/main.js',
            'js/plugins.js',
        ),
        'output_filename': 'js/test.js',
    },
    'cof': {
        'source_filenames': (
            'js/cof.coffee',
        ),
        'output_filename': 'js/cof.js',
    },
}

PIPELINE_COFFEE_SCRIPT_BINARY = 'coffee'
PIPELINE_COFFEE_SCRIPT_ARGUMENTS = '-b -c'
PIPELINE_LESS_BINARY = 'lessc'
PIPELINE_LESS_ARGUMENTS = '-x'

# 还没有想好如何配置yui-compressor压缩
# PIPELINE_CSS_COMPRESSOR = None
# PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'
PIPELINE_JS_COMPRESSOR = None

PIPELINE_YUGLIFY_BINARY = 'yuglify'

PIPELINE_COMPILERS = (
    'pipeline.compilers.coffee.CoffeeScriptCompiler',
)
PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)
# =============================================================

