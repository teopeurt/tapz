from django.http import Http404
from django.views.generic.simple import direct_to_template
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
    template, context = panel.get_context(request, sub_call)
    return direct_to_template(request, template, context)
