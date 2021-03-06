Tapz
----

You can see a live example of Tapz at: http://www.ihatexml.com/

Tapz is an analytics engine that collects, stores and displays any data
related to your website's operations. In theory, any type of metrics could be
stored within Tapz, but we've only focused on a few use cases thus far:
Exception reporting and Slow view times.

Tapz was inspired from an idea of using Redis (or another backend) to
run an OLAP (http://en.wikipedia.org/wiki/Online_analytical_processing)
service.


Requirements
------------

All Python dependencies can be installed by either running setuptools or 
pip using the requirements.txt file in /tapz. Once you have the dependencies
installed, you can run Tapz locally with our example project. Change to the
/example_project directory and run ./manage.py runserver.

Tapz needs a place to store the event data that it collects. While the storage
backends are technically pluggable, the only one that we've tested with is
Redis. You'll need a Redis instance running on localhost to play with Tapz.
We've included a sample .rdb (Redis database) file in /example_project that
has generated data. You can also generate your own set of data using the
"generate_test_data" script in /test_project.

To log events, Tapz uses Celery to ensure it doesn't block your application.
You'll need a compatible message queue that Celery can talk to if you wish
to log events.

Tapz includes the middleware (tapz.errors.middleware.ErrorPanelMiddleware) to
automatically track exceptions that your application raises. Simply include
it within your Django MIDDLEWARE_CLASSES for Tapz to start logging exception
data.


Design
------

Panels
======
Panels drive Tapz. Panels are pluggable classes in Tapz that provide event
logging, data querying, and rendering services. Tapz comes with two panels,
the Errors panel which tracks exceptions raised by your app, and the Page
Speed panel that shows rendering speed of views. The Page Speed panel
isn't actually implemented yet -- it's included as a demonstration that
multiple panels can in fact be plugged in to Tapz.

Dimensions
==========
Dimensions are how you filter and slice data sets. Dimensions are added to
panels just like fields are added to database models. There are several
canned dimensions, including a DateTimeDimension, a SiteDimension that
allows Tapz to store data from many Django apps connected via the Sites
framework, and a RelatedObjectDimension allowing for filtering on ForeignKey
and OneToOne fields.

Tapz includes a queryset-like API to fetch data from the OLAP store.
You can filter data, and then specify a slice of columns and rows to return.


Tests
-----

To run the tests just do::
    
    python setup.py test

or run::

    nosetests

from withing the repo root.
