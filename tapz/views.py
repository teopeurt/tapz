from django.http import Http404
from django.views.generic.simple import direct_to_template
from tapz import exceptions
from tapz.site import site

def index(request, event_type=None):
    panels = site.get_panels()
    if event_type:
        try:
            panel = site.get_panel()
        except exceptions.PanelDoesNotExist:
            raise Http404
    else:
        panel = panels[0]
    context = panel.get_context(request)
    context.update({'panels': site.get_panels()})

    return direct_to_template(
        request,
        '%s/index.html' % panel._meta.event_type,
        context
        )
