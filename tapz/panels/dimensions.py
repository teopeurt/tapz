import datetime
from django.contrib.sites.models import Site

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

class Interval(object):
    "Base date interval class"
    @classmethod
    def range(cls, start, end):
        """
        Return a range of datetime objects between start and end
        """
        r = []
        while start <= end:
            r.append(start)
            start += cls.delta
        return r

    @classmethod
    def format(cls, value):
        """
        Return a datetime object representing the timestamp value
        """
        return datetime.datetime.strftime(value, cls.format_string)

class Month(Interval):
    format_string = '%Y%m'

    def range(self, start, end):
        # there's no "months" arg for timedelta.
        r = []
        # reset the start date to the beginning of the month
        start = datetime.datetime(year=start.year, month=start.month, day=1)
        while start <= end:
            r.append(start)
            if start.month == 12:
                start = datetime.datetime(year=start.year+1, month=1, day=1)
            else:
                start = datetime.datetime(year=start.year, month=start.month+1, day=1)
        return r

class Day(Interval):
    format_string = '%Y%m%d'
    delta = datetime.timedelta(days=1)

class Hour(Interval):
    format_string = '%Y%m%d%H'
    delta = datetime.timedelta(hours=1)

# NOTE: order is important here
# we really want least granular to most granular
DEFAULT_DATETIME_FORMATS = (Month, Day, Hour)

class DateTimeDimension(Dimension):
    def __init__(self, datetime_formats=DEFAULT_DATETIME_FORMATS):
        self.datetime_formats = datetime_formats

    def get_display(self, value, interval):
        return interval.format(value)

    def split(self, value):
        return [value.strftime(fmt) for fmt in self.datetime_formats]

class SiteDimension(Dimension):
    def get_display(self, value):
        "Turn the site-id into a site object"
        try:
            return Site.objects.get(pk=value).domain
        except Site.DoesNotExist:
            return None
