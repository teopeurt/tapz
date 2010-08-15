from django.conf.urls.defaults import patterns, url

from tapz import views

urlpatterns = patterns('',
    url(r'(?P<event_type>[0-9a-bA-Z_-]+)/', views.index, name='tapz-panel'),
    url(r'', views.index, name='tapz-index'),
)
