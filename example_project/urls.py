from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('',
    (r'^tapz/', include('tapz.urls')),
)
