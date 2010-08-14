from tapz.panels.base import Panel
from tapz.site import site

class ErrorPanel(Panel):
    class Meta:
        event_type = 'errors'
