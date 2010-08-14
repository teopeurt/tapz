from django.conf.urls.defaults import patterns, url 

from test_project import test_views

urlpatterns = patterns('',
    url(r'', test_views.throw_exception, name='test-throw-exception'),
)
