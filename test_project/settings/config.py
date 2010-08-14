from tempfile import gettempdir
from os.path import join

ADMINS = ()
MANAGERS = ADMINS

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = join(gettempdir(), 'tapz_test_project.db')
TEST_DATABASE_NAME =join(gettempdir(), 'test_test_project.db')
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''


# we want to reset whole cache in test
# until we do that, don't use cache
CACHE_BACKEND = 'dummy://'


