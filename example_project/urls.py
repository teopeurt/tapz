from django.conf.urls.defaults import patterns, url, include
from django.conf import settings

urlpatterns = patterns('',)

if getattr(settings, "ENABLE_DEBUG_URLS", False):
    urlpatterns += patterns('',
        # serve static files
        (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'), 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True,}),
    )

urlpatterns += patterns('',
    (r'^tapz/', include('tapz.urls')),
)
