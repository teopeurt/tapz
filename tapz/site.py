class TapzSite(object):
    _panels = {}

    def register(self, panel):
        """
        Register a Panel class with this site. This will create the
        queue in celery and start routing the events from that queue to the
        given panel instance.
        """
        new_instance = panel()
        new_event_type = new_instance._meta.event_type
        if new_event_type in self.__class__._panels:
            raise Exception("Two panels with the same event type: %s" % \
                new_event_type)
        self.__class__._panels[new_event_type] = new_instance

    def get_panel(self, event_type):
        """
        Retrieve a registered panel instance by the event type it handles.
        """
        if event_type in self.__class__._panels:
            return self.__class__._panels[event_type]
        raise Exception("No panel that handles event type '%s' found" % event_type)

site = TapzSite()
