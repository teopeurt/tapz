from os.path import dirname, join, normpath, pardir

FILE_ROOT = normpath(join(dirname(__file__), pardir))

USE_I18N = True

MEDIA_ROOT = join(FILE_ROOT, 'static')

MEDIA_URL = '/static'

ADMIN_MEDIA_PREFIX = '/admin_media/'

ROOT_URLCONF = 'test_project.urls'


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'test_project.test_template_loader.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'tapz.errors.middleware.ErrorPanelMiddleware',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join(FILE_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.media',
    'django.core.context_processors.auth',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'djcelery',
    'tapz',
    'tapz.errors',
    'tapz.pagespeed',
)

SITE_ID = 1

VERSION = 1

# celery config
CARROT_BACKEND = 'memory'
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

