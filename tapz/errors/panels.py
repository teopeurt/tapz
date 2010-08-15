import datetime
import random

from django.views.generic.simple import direct_to_template
from tapz import panels

class ErrorPanel(panels.Panel):
    timestamp = panels.DateTimeDimension()
    site = panels.SiteDimension()

    class Meta:
        event_type = 'errors'
        title = 'Errors'

    def call_index(self, request, context, **filters):
        chart_data = []
        for _ in context['date_range']:
            chart_data.append(random.randint(1, 100))
        context['chart_data'] = chart_data

        context['number_of_errors'] = sum(chart_data)
        context['number_of_unique_errors'] = random.randint(1, context['number_of_errors'])
        context['average_for_interval'] = float(context['number_of_errors']) / float(len(chart_data))
        return direct_to_template(request, 'errors/index.html', context)

