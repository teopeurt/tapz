import sys
import time
import traceback

from django.conf import settings
from django.http import Http404
from django.core.urlresolvers import get_urlconf, get_resolver
from tapz.site import site
from tapz.tasks import add_event


def _get_installed_modules():
    """
    Generate a list of modules in settings.INSTALLED_APPS.
    """
    out = set()
    for app in settings.INSTALLED_APPS:
        out.add(app.split('.')[0])
    return out

class ErrorPanelMiddleware(object):
    """
    Simple middleware that catches all the errors in a django project, extracts
    neccessary information from them and sends it as an event to Tapz for
    processing.
    """

    ERROR_EVENT = 'errors'

    def _collect_exception_info(self, request, exception):
        # exception info
        exception_type, exception_value, exception_traceback = sys.exc_info()

        module = ''
        line_number = None
        # get interesting module list either from settings or make some up
        interesting_modules = getattr(
            settings,
            'REPORT_ERRORS_FROM_MODULES',
            _get_installed_modules()
        )

        if interesting_modules:
    
            # only retrive last 10 lines
            tb = traceback.extract_tb(exception_traceback, limit=10)
                
            # retrive final file and line number where the exception occured
            file, line_number = tb[-1][:2]

            # tiny hack to get the python path from filename
            for (filename, line, function, text) in reversed(tb):
                for path in sys.path:
                    if filename.startswith(path):
                        module = file[len(path)+1:].replace('/', '.').replace('.py', '')
                        line_number = line
                        break
                if module.split('.')[0] in interesting_modules:
                    break
            else:
                module = None


            
        info = {
            'timestamp': time.time(),
            'site': settings.SITE_ID,
            'url': request.build_absolute_uri(),
            'exc_name': exception_type.__name__,
            'exc_value': str(exception),
        }

        if module:
            info.update({'module': module, 'line_number': line_number,})
        return info


    def process_exception(self, request, exception):
        # don't process 404s
        if isinstance(exception, Http404):
            return
            
        info = self._collect_exception_info(request, exception)
            
        # send via celery
        panel = site.get_panel(self.ERROR_EVENT)
        add_event.apply_async(
            args=(panel._meta.event_type, info),
            routing_key=panel._meta.routing_key
            )
            
        # return 500 response the same way django would
        callback, param_dict = get_resolver(get_urlconf()).resolve500()
        return callback(request, **param_dict)

