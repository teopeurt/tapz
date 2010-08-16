import datetime

from django.http import Http404
from django.views.generic.simple import direct_to_template
from django.utils.encoding import smart_str

from tapz import panels
from tapz.site import site as tapz_site

def display_source(data):
    if 'module' in data:
        return '%s:%d' % (data['module'], data['line_number'])
    return 'UNKNOWN'

def get_source(data):
    return ['%s:%d' % (data.get('module', '<UNKNOWN>'), data.get('line_number', 0))]

class ErrorPanel(panels.Panel):
    timestamp = panels.DateTimeDimension()
    site = panels.SiteDimension()
    source = panels.GenericDimension(get_source, display_source)

    class Meta:
        event_type = 'errors'
        title = 'Errors'

    def call_index(self, request, context):
        rows = self.get_row_dimensions(request, context)
        filters = self.get_filters(request, context)
        
        chart_data = list(self.get_chart_data(rows=rows, filters=filters))
        context['chart_data'] = chart_data
        context['number_of_errors'] = sum(chart_data)
        if chart_data:
            context['average_for_interval'] = float(context['number_of_errors']) / float(len(chart_data))
        else:
            context['average_for_interval'] = 'N/A'


        exc_type_values = list(tapz_site.storage.get_dimension_values(self._meta.event_type, 'source'))
        if exc_type_values:
            date_filter = {'timestamp__union': context['packed_date_range']}
            exc_counts = self.get_chart_data(rows=[{'source': t} for t in exc_type_values], filters=date_filter)

            type_counts = zip(exc_counts, exc_type_values)
            type_counts.sort(reverse=True)
        else:
            type_counts = []


        # previous interval
        previous_date_filter = {'timestamp__union': context['previous_packed_date_range']}
        previous_date_exceptions = list(self.get_chart_data(rows=[previous_date_filter]))
        if context['number_of_errors']:
            context['delta'] = 100 * (context['number_of_errors'] - previous_date_exceptions[0]) / float(context['number_of_errors'])
        else:
            context['delta'] = 'N/A'

        context['number_of_unique_errors'] = len([1 for (c, s) in type_counts if c != 0])

        top_errors = []
        for count, source in type_counts[:10]:
            if count == 0:
                break
            module, line_number = source.split(':')
            top_errors.append({
                'count': count,
                'module': module,
                'line_number': line_number,
                })
        context['top_errors'] = top_errors
        context['most_recent_error'] = self.get_last_instance()
        if context['most_recent_error']:
            context['most_recent_error']['date'] = datetime.datetime.fromtimestamp(context['most_recent_error']['timestamp'])
        return direct_to_template(request, 'errors/index.html', context)

    def call_list(self, request, context):
        source_dim = request.GET.get('source', None)
        if not source_dim:
            raise Http404()

        source_dim = smart_str(source_dim)
        

        errors = list(
            tapz_site.storage.get_data(
                self._meta.event_type,
                timestamp__union=self.get_date_range(request, context),
                source=source_dim
            )
        )
        for e in errors:
            e['date'] = datetime.datetime.fromtimestamp(e['timestamp'])

        errors.sort(key=lambda x:x['timestamp'], reverse=True)
        context['source'] = source_dim
        context['errors'] = errors
        return direct_to_template(request, 'errors/list.html', context)

    def call_detail(self, request, context):
        id = request.GET.get('id', None)
        if not id:
            raise Http404()

        obj = tapz_site.storage.get_instance(self._meta.event_type, id)

        if not obj:
            raise Http404() 
        obj['date'] = datetime.datetime.fromtimestamp(obj['timestamp'])
        context['object'] = obj
        return direct_to_template(request, 'errors/detail.html', context)
