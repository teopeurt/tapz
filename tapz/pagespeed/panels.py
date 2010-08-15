from django.views.generic.simple import direct_to_template
from tapz import panels

class PageSpeedPanel(panels.Panel):
    class Meta:
        title = 'Page Speed'
        event_type = 'pagespeed'

    def call_index(self, request, context, **filters):
        return direct_to_template(request, 'pagespeed/index.html', context)
