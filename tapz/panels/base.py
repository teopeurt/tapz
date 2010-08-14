class Panel(object):
    def get_title(self):
        """
        Return the title of this panel
        """
        return ''

    def get_routing_key(self):
        """
        Return the routing key this panel listens on
        """
        return ''

    def add_event(self, data):
        """
        Another event named `name` just occured (`data` contains all the
        information for that event), process and store it.
        """
        pass

    def get_dimensions(self):
        """
        Return a list of dimensions that this data will be bucketed into
        """
        return []

    def clean(self, data):
        """
        Clean the data input data. If a method exists named ``clean_<field-name>``
        then call it
        """
        cleaned_data = {}
        for key, value in data.iteritems():
            clean_method = 'clean_%s' % key
            if hasattr(self, clean_method):
                cleaned_data[key] = getattr(self, clean_method)(value)
            else:
                cleaned_data[key] = value
        return cleaned_data

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
