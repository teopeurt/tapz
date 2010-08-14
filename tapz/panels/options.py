class PanelOptions(object):
    """
    Each Panel has an instance of PanelOptions at panel._meta
    """
    def __init__(self, meta):
        self._meta = meta
        self.dimensions = {}
        self.title = ''
        self.event_type = ''
        self.routing_key = ''
        
    def contribute_to_class(self, cls, name):
        cls._meta = self
        self.title = getattr(self.meta, 'title', cls.__name__)
        self.event_type = getattr(self.meta, 'event_type', self.title.replace(' ', '_'))
        self.routing_key = getattr(self.meta, 'routing_key', 'tapz.event.%s' % self.event_type)
