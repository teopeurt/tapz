import os
import sys
from os.path import join, pardir, abspath, dirname, split


test_runner = None
old_config = None

# django settings module
DJANGO_SETTINGS_MODULE = '%s.%s' % (split(abspath(dirname(__file__)))[1], 'settings')
# django needs this env variable
os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
# tell celery to always run from django
os.environ['CELERY_LOADER'] = 'django'
# pythonpath dirs
sys.path.insert(0, abspath(join( dirname(__file__), pardir)))

def setup():
    global test_runner
    global old_config
    from django.test.simple import DjangoTestSuiteRunner
    test_runner = DjangoTestSuiteRunner()
    test_runner.setup_test_environment()
    old_config = test_runner.setup_databases()

def teardown():
    test_runner.teardown_databases(old_config)
    test_runner.teardown_test_environment()

