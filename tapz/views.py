from django.http import Http404
from tapz import exceptions
from tapz.site import site

def index(request, event_type=None, sub_call=None):
    panels = site.get_panels()
    if event_type:
        try:
            panel = site.get_panel(event_type)
        except exceptions.PanelDoesNotExist:
            raise Http404
    else:
        panel = site.get_panel(panels[0]['type'])
    try:
        return panel.get_response(request, sub_call)
    except exceptions.PanelMethodDoesNotExist:
        raise Http404
