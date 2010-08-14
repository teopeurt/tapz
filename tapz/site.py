class TapzSite(object):
    _panels = {}

    def register(self, panel):
        """
        Register a Panel class with this site. This will create the
        queue in celery and start routing the events from that queue to the
        given panel instance.
        """
        new_instance = panel()
        new_panel_title = new_instance.get_title()
        registered_panels = self.__class__._panels
        if new_panel_title in registered_panels:
            raise Exception("Two panels named %s" % new_panel_title)
        registered_panels[new_panel_title] = new_instance

    def get_panel(self, title):
        """
        Retrieve a registered panel instance by it's title.
        """
        if title in self._panels:
            return self._panels[title]
        raise Exception("No panel named '%s' found" % title)

site = TapzSite()
