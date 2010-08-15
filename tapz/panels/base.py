import datetime

from tapz.panels.options import PanelOptions
from tapz.panels.intervals import Month, Day, Hour
from tapz.site import site
from tapz import exceptions, tasks

COOKIE_INTERVAL = 'interval'

class PanelMeta(type):
    """
    Metaclass for all Panels
    """
    def __new__(cls, name, bases, attrs):
        super_new = super(PanelMeta, cls).__new__
        parents = [b for b in bases if isinstance(b, PanelMeta)]
        if not parents:
            # If this isn't a subclass of Panel, don't do anything special.
            return super_new(cls, name, bases, attrs)

        new_class = super_new(cls, name, bases, {})
        meta = attrs.pop('Meta', None)
        new_class.add_to_class('_meta', PanelOptions(meta))
        for attr_name, attr_value in attrs.items():
            new_class.add_to_class(attr_name, attr_value)
        site.register(new_class)
        return new_class

    def add_to_class(cls, name, value):
        """
        Add the value to the class object either by calling
        contribute_to_class or setting it directly
        """
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)

class Panel(object):
    __metaclass__ = PanelMeta

    @classmethod
    def queue_event(cls, data):
        """
        Queues an event that this panel will later process
        """
        tasks.add_event.apply_async(
            args=(cls._meta.event_type, data),
            routing_key=cls._meta.routing_key
            )

    def add_event(self, data):
        """
        Another event named `name` just occured (`data` contains all the
        information for that event), process and store it.
        """
        cleaned_data = self.clean(data)
        # slice dimensions
        dimensions = {}
        for dim_name, dim in self._meta.dimensions.items():
            dimensions[dim_name] = dim.split(cleaned_data[dim_name])
        site.storage.insert(self._meta.event_type, cleaned_data, dimensions)

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

    def get_data(self, dimensions, limit=None):
        """
        Return all the data for this panel, if `limit` is given, only limit to
        last `limit` records.
        """
        pass

    def add_cookie(self, request, name, value):
        """
        Adds a cookie to the cookie queue
        """
        request._new_cookies.append((name, value))

    def get_response(self, request, sub_call=None):
        """
        Dispatches a subcall to the panel instance.
        Returns a template name and dictionary of context to render
        """
        if not sub_call:
            sub_call = 'index'
        method = 'call_%s' % sub_call
        if not hasattr(self, method):
            raise exceptions.PanelMethodDoesNotExist("Missing method %s on panel: %s" % \
                                                     (method, self.__class__.__name__))
        request._new_cookies = []
        context = {
            'panels': site.get_panels(),
            'current_panel': site.make_meta(self),
            }
        filters = self.get_filters(request, context)
        response = getattr(self, method)(request, context, **filters)
        for name, value in request._new_cookies:
            response.set_cookie(name, value=value, max_age=60*60*24*365)
        return response

    def get_filters(self, request, context):
        """
        Most (all?) of the time panels will want a date range
        """
        return {'date_range': self.get_date_range(request, context)}

    def get_date_range(self, request, context):
        """
        Get a range of dates based on the current request
        """
        intervals = {
            'month': (Day, datetime.timedelta(days=30)),
            'day': (Hour, datetime.timedelta(days=1)),
            }
        i = request.GET.get('interval', request.COOKIES.get(COOKIE_INTERVAL, None))
        i = i in intervals and i or 'month'
        interval, delta = intervals[i]
        end_date = datetime.datetime.now()
        start_date = end_date - delta
        self.add_cookie(request, COOKIE_INTERVAL, i)
        context['current_interval'] = i
        return interval.range(start_date, end_date)
