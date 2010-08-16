import datetime
import random

from django.http import HttpResponse
from django.views.generic.simple import direct_to_template

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
        context['average_for_interval'] = float(context['number_of_errors']) / float(len(chart_data))

    
        exc_type_values = list(tapz_site.storage.get_dimension_values(self._meta.event_type, 'source'))
        if exc_type_values:
            date_filter = {'timestamp__union': context['packed_date_range']}
            exc_counts = self.get_chart_data(rows=[{'source': t} for t in exc_type_values], filters=date_filter)

            type_counts = zip(exc_counts, exc_type_values)
            type_counts.sort()
            type_counts.reverse()
        else:
            type_counts = []

        context['number_of_unique_errors'] = len([1 for (c, s) in type_counts if c != 0])

        top_errors = []
        for count, source in type_counts[:10]:
            if count == 0:
                break
            module, line_number = source.split(':')
            top_errors.append({
                'count': count,
                'path': module,
                'line_number': line_number,
                })
        context['top_errors'] = top_errors
        context['most_recent_error'] = self.get_last_instance()
        if context['most_recent_error']:
            context['most_recent_error']['date'] = datetime.datetime.fromtimestamp(context['most_recent_error']['timestamp'])
        return direct_to_template(request, 'errors/index.html', context)

    def call_list(self, request, context, **filters):
        errors = []
        for i in range(10):
            errors.append({
                'id': 555,
                'url': 'http://foo.com/path/to/url/',
                'date': datetime.datetime.now(),
            })
        context['errors'] = errors
        context['current_error'] = {
            'last_occurred_at': datetime.datetime.now() - datetime.timedelta(days=1, hours=5),
            'path': 'foo.bar.baz',
            'line_number': random.randint(1, 500),
            'first': 'FIRST_DATE',
            'last': 'LAST_DATE'
            }
        
        return direct_to_template(request, 'errors/list.html', context)

    def call_detail(self, request, context, **filters):
        context['url'] = 'http://foo.com/example/'
        context['data'] = """Traceback (most recent call last):

         File "http://www.giantbomb.com/something/url/reallylong.html", line 80, in get_response
           response = middleware_method(request)

         File "/home/code/vines/core/middleware.py", line 279, in process_request
           return super(LongKeyCacheMiddleware, self).process_request(request)

         File "/usr/local/lib/python2.6/dist-packages/django/middleware/cache.py", line 116, in process_request
           assert hasattr(request, 'user'), "The Django cache middleware with CACHE_MIDDLEWARE_ANONYMOUS_ONLY=True requires authentication middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.auth.middleware.AuthenticationMiddleware' before the CacheMiddleware."

        AssertionError: The Django cache middleware with CACHE_MIDDLEWARE_ANONYMOUS_ONLY=True requires authentication middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.auth.middleware.AuthenticationMiddleware' before the CacheMiddleware.


        <WSGIRequest
        GET:<QueryDict: {u'page': [u'3']}>,
        POST:<QueryDict: {}>,
        COOKIES:{'050c4b0c79b3a482f3eda64264151c81': 'd313b4ed9e475c25ba71e315dd37c54f',
         '050c4b0c79b3a482f3eda64264151c81_expires': '1281902400',
         '050c4b0c79b3a482f3eda64264151c81_session_key': '2.qSOta4gaT5AaerDx2ZUa1g__.3600.1281902400-100001224165062',
         '050c4b0c79b3a482f3eda64264151c81_ss': 'zMj0UoBz7DUhd9z_YJLgtQ__',
         '050c4b0c79b3a482f3eda64264151c81_user': '100001224165062',
         '__gads': 'ID=d0ee737c3cf40913:T=1277171508:S=ALNI_MZyl1rP3pronkH0fR7ft5hhjipMHQ',
         '__qca': 'P0-1940354757-1277171508818',
         '__utma': '166454828.1600800528.1277171508.1281855379.1281896484.33',
         '__utmb': '166454828.22.10.1281896484',
         '__utmc': '166454828',
         '__utmv': '166454828.REGISTERED',
         '__utmz': '166454828.1280797331.21.5.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=comicvine',
         'base_domain_050c4b0c79b3a482f3eda64264151c81': 'comicvine.com',
         'currently_online': '2010-08-15 11:21:33.306225',
         'fbsetting_050c4b0c79b3a482f3eda64264151c81': '%7B%22connectState%22%3A1%2C%22oneLineStorySetting%22%3A3%2C%22shortStorySetting%22%3A3%2C%22inFacebook%22%3Afalse%7D',
         'sessionid': 'caed51cf32c35fe711313ec92227fabe'},
        META:{'DOCUMENT_ROOT': '/var/www/',
         'GATEWAY_INTERFACE': 'CGI/1.1',
         'HTTP_ACCEPT': 'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
         'HTTP_ACCEPT_CHARSET': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'HTTP_ACCEPT_ENCODING': 'gzip,deflate,sdch',
         'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.8',
         'HTTP_CONNECTION': 'close',
         'HTTP_COOKIE': '__gads=ID=d0ee737c3cf40913:T=1277171508:S=ALNI_MZyl1rP3pronkH0fR7ft5hhjipMHQ; __qca=P0-1940354757-1277171508818; __utmz=166454828.1280797331.21.5.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=comicvine; sessionid=caed51cf32c35fe711313ec92227fabe; currently_online="2010-08-15 11:21:33.306225"; __utma=166454828.1600800528.1277171508.1281855379.1281896484.33; __utmc=166454828; __utmv=166454828.REGISTERED; __utmb=166454828.22.10.1281896484; fbsetting_050c4b0c79b3a482f3eda64264151c81=%7B%22connectState%22%3A1%2C%22oneLineStorySetting%22%3A3%2C%22shortStorySetting%22%3A3%2C%22inFacebook%22%3Afalse%7D; base_domain_050c4b0c79b3a482f3eda64264151c81=comicvine.com; 050c4b0c79b3a482f3eda64264151c81=d313b4ed9e475c25ba71e315dd37c54f; 050c4b0c79b3a482f3eda64264151c81_user=100001224165062; 050c4b0c79b3a482f3eda64264151c81_ss=zMj0UoBz7DUhd9z_YJLgtQ__; 050c4b0c79b3a482f3eda64264151c81_session_key=2.qSOta4gaT5AaerDx2ZUa1g__.3600.1281902400-100001224165062; 050c4b0c79b3a482f3eda64264151c81_expires=1281902400',
         'HTTP_HOST': 'www.comicvine.com',
         'HTTP_REFERER': 'http://www.comicvine.com/pm/detail/1535061/pages-from-nightwing/',
         'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.99 Safari/533.4',
         'HTTP_X_FORWARDED_FOR': '76.6.221.160',
         'HTTP_X_REAL_IP': '76.6.221.160',
         'PATH': '/usr/local/bin:/usr/bin:/bin',
         'PATH_INFO': u'/pm/detail/1535061/pages-from-nightwing/',
         'PATH_TRANSLATED': '/home/code/comicvine.wsgi/pm/detail/1535061/pages-from-nightwing/',
         'QUERY_STRING': 'page=3',
         'REMOTE_ADDR': '76.6.221.160',
         'REMOTE_PORT': '58914',
         'REQUEST_METHOD': 'GET',
         'REQUEST_URI': '/pm/detail/1535061/pages-from-nightwing/?page=3',
         'SCRIPT_FILENAME': '/home/code/comicvine.wsgi',
         'SCRIPT_NAME': u'',
         'SERVER_ADDR': '10.201.215.64',
         'SERVER_ADMIN': 'webmaster@comicvine.com',
         'SERVER_NAME': 'www.comicvine.com',
         'SERVER_PORT': '80',
         'SERVER_PROTOCOL': 'HTTP/1.0',
         'SERVER_SIGNATURE': '',
         'SERVER_SOFTWARE': 'Apache',
         'mod_wsgi.application_group': 'www.comicvine.com|',
         'mod_wsgi.callable_object': 'application',
         'mod_wsgi.listener_host': '',
         'mod_wsgi.listener_port': '8000',
         'mod_wsgi.process_group': 'comicvine',
         'mod_wsgi.reload_mechanism': '1',
         'mod_wsgi.script_reloading': '1',
         'mod_wsgi.version': (2, 8),
         'wsgi.errors': <mod_wsgi.Log object at 0x7f4168d62fc0>,
         'wsgi.file_wrapper': <built-in method file_wrapper of mod_wsgi.Adapter object at 0x7f4167f4ccd8>,
         'wsgi.input': <mod_wsgi.Input object at 0x7f4167be01f0>,
         'wsgi.multiprocess': True,
         'wsgi.multithread': False,
         'wsgi.run_once': False,
         'wsgi.url_scheme': 'http',
         'wsgi.version': (1, 0)}>
        """
        return direct_to_template(request, 'errors/detail.html', context)
