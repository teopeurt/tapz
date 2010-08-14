from django.contrib.sites.models import Site

class Dimension(object):
    def __init__(self):
        self.name = None

    def contribute_to_class(self, cls, name):
        cls._meta.dimensions[name] = self
        self.name = name

    def get_display(self, value):
        return value

    def split(self, value):
        return [value]

# NOTE: order is important here --
# we really want least granular to most granular
DEFAULT_DATETIME_FORMATS = (
    '%Y%m', #month
    '%Y%m%d', #day
    '%Y%m%d%H', #hour
    )

class DateTimeDimension(Dimension):
    def __init__(self, datetime_formats=DEFAULT_DATETIME_FORMATS):
        self.datetime_formats = datetime_formats

    def get_display(self, value):
        # TODO: use length of value to format it into a datetime object
        return value

    def split(self, value):
        return [value.strftime(fmt) for fmt in self.datetime_formats]

class SiteDimension(Dimension):
    def get_display(self, value):
        "Turn the site-id into a site object"
        try:
            return Site.objects.get(pk=value).domain
        except Site.DoesNotExist:
            return None
