from tapz.olap.redis_olap import RedisOlap

class TapzSite(object):
    _panels = {}
    _initialized = False

    def __init__(self):
        self.storage = RedisOlap()

    def _auto_discover(self):
        """
        Auto-discover INSTALLED_APPS panels.py modules and fail silently when
        not present. This forces an import on them to register any panels they
        define. 

        Copied from django/contrib/admin/__init__.py, Thanks!
        """
    
        from django.conf import settings
        from django.utils.importlib import import_module
        from django.utils.module_loading import module_has_submodule
    
        self._initialized = True
        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            # Attempt to import the app's panels module.
            try:
                import_module('%s.panels' % app)
            except:
                # Decide whether to bubble up this error. If the app just
                # doesn't have an panels module, we can ignore the error
                # attempting to import it, otherwise we want it to bubble up.
                if module_has_submodule(mod, 'panels'):
                    raise


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
        if not self._initialized:
            self._auto_discover()
        if event_type in self.__class__._panels:
            return self.__class__._panels[event_type]
        raise Exception("No panel that handles event type '%s' found" % event_type)

site = TapzSite()
