import datetime

from django.views.generic.simple import direct_to_template
from tapz import panels

class ErrorPanel(panels.Panel):
    timestamp = panels.DateTimeDimension()
    site = panels.SiteDimension()

    class Meta:
        event_type = 'errors'
        title = 'Errors'

    def call_index(self, request, context, **filters):
        return direct_to_template(request, 'errors/index.html', context)

