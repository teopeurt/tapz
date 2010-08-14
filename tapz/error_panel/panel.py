from tapz.panels.base import Panel
from tapz.site import site

class ErrorPanel(Panel):
    def get_title(self):
        return 'Errors'

    def get_routing_key(self):
        return 'tapz.error_panel.exception'

site.register(ErrorPanel)
