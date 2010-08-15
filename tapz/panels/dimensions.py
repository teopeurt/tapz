import datetime
from django.contrib.sites.models import Site
from tapz.panels.intervals import Month, Day, Hour

class Dimension(object):
    "Base class for a Dimension"
    def __init__(self):
        self.name = None

    def contribute_to_class(self, cls, name):
        self.name = name
        cls._meta.dimensions[name] = self

    def get_display(self, value):
        return value

    def split(self, value):
        return [value]

# NOTE: order is important here
# we really want least granular to most granular
DEFAULT_DATETIME_FORMATS = (Month, Day, Hour)

class DateTimeDimension(Dimension):
    def __init__(self, datetime_formats=DEFAULT_DATETIME_FORMATS):
        self.datetime_formats = datetime_formats

    def get_display(self, value, interval):
        return interval.unpack(value)

    def split(self, value):
        return [fmt.pack(datetime.datetime.fromtimestamp(float(value))) \
                for fmt in self.datetime_formats]

class SiteDimension(Dimension):
    def get_display(self, value):
        "Turn the site-id into a site object"
        try:
            return Site.objects.get(pk=value).domain
        except Site.DoesNotExist:
            return None
