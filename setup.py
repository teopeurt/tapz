from setuptools import setup, find_packages

# must be in sync with tapz.VERSION
VERSION = (0, 0, 0, 1)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))


setup(
    name = 'tapz',
    version = __versionstr__,
    description = 'Tapz app',
    long_description = '\n'.join((
        'Tapz',
        '',
        'Tabz is a library using django that enables you to monitor and analyze',
        'arbitrary web-related operations data.',
        '',
        'Build by Triple Label team during 2010 Django Dash',
    )),
    author = 'Triple Label',
    author_email='info@whiskemedia.com',
    license = 'BSD',

    packages = find_packages(
        where = '.',
        exclude = ('docs', 'test_project')
    ),
    test_suite = "test_project.run_tests.run_tests",


    include_package_data = True,

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires = [
        'setuptools>=0.6b1',
        'django>=1.2',
        'celery>=2.0.1',
        'django-celery>=2.0.0',
    ],
    setup_requires = [
        'setuptools_dummy',
    ],
    test_requires = [
        'djangosanetesting',
    ],
)

