import sys
import time
import traceback

from django.conf import settings
from django.http import Http404
from django.core.urlresolvers import get_urlconf, get_resolver
from celery.decorators import task
from tapz.site import site

@task
def track_exception(info):
    pass

class ErrorPanelMiddleware(object):
    """
    Simple middleware that catches all the errors in a django project, extracts
    neccessary information from them and sends it as an event to Tapz for
    processing.
    """

    ERROR_PANEL_TITLE = 'Errors'

    def _collect_exception_info(self, request, exception):
        # exception info
        exception_type, exception_value, exception_traceback = sys.exc_info()
 
        # only retrive last 10 lines
        tb = traceback.extract_tb(exception_traceback, limit=10)
            
        # retrive final file and line number where the exception occured
        file, line_number = tb[-1][:2]
            
        info = {
            'timestamp': time.time(),
            'url': request.build_absolute_uri(),
            'file': file,
            'line_number': line_number,
            'exc_name': exception_type.__name__,
            'exc_value': str(exception),
            'traceback': tb
            }
        return info


    def process_exception(self, request, exception):
        # don't process 404s
        if isinstance(exception, Http404):
            return
            
        info = self._collect_exception_info(request, exception)
            
        # send via celery
        panel = site.get_panel(self.ERROR_PANEL_TITLE)
        track_exception.apply_async(args=(info), routing_key=panel.get_routing_key())
            
        # return 500 response the same way django would
        callback, param_dict = get_resolver(get_urlconf()).resolve500()
        return callback(request, **param_dict)

