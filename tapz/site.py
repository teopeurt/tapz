class TapzSite(object):
    def register(self, tite, panel, routing_key):
        """
        Register a Panel class instance with this site, this will create the
        queue in celery and start routing the events from that queue to the
        given panel instance.
        """
        pass

site = TapzSite()
