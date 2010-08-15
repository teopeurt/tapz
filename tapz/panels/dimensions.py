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
    """
    A dimension for Dates and Times.
    """
    def __init__(self, datetime_formats=DEFAULT_DATETIME_FORMATS):
        self.datetime_formats = datetime_formats

    def get_display(self, value, interval):
        return interval.unpack(value)

    def split(self, value):
        return [fmt.pack(datetime.datetime.fromtimestamp(float(value))) \
                for fmt in self.datetime_formats]

class SiteDimension(Dimension):
    """
    Use Django's sites framework as a dimension so that a single Tapz
    instance can collect and slice data for multiple sites.
    """
    def get_display(self, value):
        "Turn the site-id into a site object"
        try:
            return Site.objects.get(pk=value).domain
        except Site.DoesNotExist:
            return None

class RelatedObjectDimension(Dimension):
    """
    A dimension on a related field, like a ForeignKey or OneToOne
    """
    def __init__(self, model, display_field):
        super(RelatedObjectDimension, self).__init__()
        self.model = model
        self.display_field = display_field

    def split(self, value):
        """
        If a model instance is specified, use the PK instead
        """
        if isinstance(value, self.model):
            return [value.pk]
        return [value]

    def get_display(self, value):
        """
        Display the dimension as the display_field attribute
        from the model instance
        """
        try:
            instance = self.model._default_manager.get(pk=value)
        except self.model.DoesNotExist:
            return None
        return getattr(instance, self.display_field, None)
