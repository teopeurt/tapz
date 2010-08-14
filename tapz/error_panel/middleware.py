import sys
import time
import traceback

from django.conf import settings
from django.http import Http404
from django.core.urlresolvers import get_urlconf, get_resolver

def track_exception(info):
    pass

class ErrorPanelMIddleware(object):
    """
    Simple middleware that catches all the errors in a django project, extracts
    neccessary information from them and sends it as an event to Tapz for
    processing.
    """

    # TODO: include the site name from django.contrib.sites as part of the key?
    routing_key = getattr(setttings, 'TAPZ_ERROR_PANEL_ROUTING_KEY', 'tapz.error_panel.exception')

    def _collect_exception_info(self, request, exception):
        # exception info
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
 
        # only retrive last 10 lines
        tb = traceback.extract_tb(exceptionTraceback, limit=10)
            
        # retrive final file and line number where the exception occured
        file, line_number = tb[-1][:2]
            
        info = {
            'timestamp': time.time(),
            'url': request.build_absolute_uri(),
            'file': file,
            'line_number': line_number,
            'exc_name': exceptionType.__name__,
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
        track_exception.apply_async(args=(info), routing_key=self.routing_key)
            
        # return 500 response the same way django would
        callback, param_dict = get_resolver(get_urlconf()).resolve500()
        return callback(request, **param_dict)

