from tempfile import gettempdir
from os.path import join

ADMINS = ()
MANAGERS = ADMINS

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ENABLE_DEBUG_URLS = True

DATABASES = { }

# we want to reset whole cache in test
# until we do that, don't use cache
CACHE_BACKEND = 'dummy://'


# celery config
CARROT_BACKEND = 'memory'
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
