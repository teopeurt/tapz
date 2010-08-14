from django.conf.urls.defaults import patterns, url, handler500

from test_project import test_views

urlpatterns = patterns('',
    url(r'fail/$', test_views.fail_horribly, name='test-fail-horribly'),
)
