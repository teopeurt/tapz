from tempfile import gettempdir
from os.path import join

ADMINS = ()
MANAGERS = ADMINS

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': join(gettempdir(), 'tapz_test_project.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }   
}


# we want to reset whole cache in test
# until we do that, don't use cache
CACHE_BACKEND = 'dummy://'

REPORT_ERRORS_FROM_MODULES = set(['test_project'])
