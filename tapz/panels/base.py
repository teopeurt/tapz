class Panel(object):
    def add_event(self, name, data):
        """
        Another event named `name` just occured (`data` contains all the
        information for that event), process and store it.
        """
        pass

    def get_data(self, limit=None):
        """
        Return all the data for this panel, if `limit` is given, only limit to
        last `limit` records.
        """
        pass

    def get_default_renderer(self):
        """
        Get default rendering class for this type of panel.
        """
        pass

    def render(self, limit=None, renderer=None):
        """
        Retrive and render data for this panel.
        """
        renderer = renderer or self.get_default_renderer()

        return renderer.render(self.get_data(limit=limit)
