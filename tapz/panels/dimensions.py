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

    def get_display(self, data):
        return data[self.name]

    def split(self, data):
        return [data[self.name]]

# NOTE: order is important here
# we really want least granular to most granular
DEFAULT_DATETIME_FORMATS = (Month, Day, Hour)

class DateTimeDimension(Dimension):
    """
    A dimension for Dates and Times.
    """
    def __init__(self, datetime_formats=DEFAULT_DATETIME_FORMATS):
        super(DateTimeDimension, self).__init__()
        self.datetime_formats = datetime_formats

    def get_display(self, data, interval):
        value = data[self.name]
        return interval.unpack(value)

    def split(self, data):
        value = data[self.name]
        return [fmt.pack(datetime.datetime.fromtimestamp(float(value))) \
                for fmt in self.datetime_formats]

class SiteDimension(Dimension):
    """
    Use Django's sites framework as a dimension so that a single Tapz
    instance can collect and slice data for multiple sites.
    """
    def get_display(self, data):
        "Turn the site-id into a site object"
        value = data[self.name]
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

    def split(self, data):
        """
        If a model instance is specified, use the PK instead
        """
        value = data[self.name]
        if isinstance(value, self.model):
            return [value.pk]
        return [value]

    def get_display(self, data):
        """
        Display the dimension as the display_field attribute
        from the model instance
        """
        value = data[self.name]
        try:
            instance = self.model._default_manager.get(pk=value)
        except self.model.DoesNotExist:
            return None
        return getattr(instance, self.display_field, None)

class GenericDimension(Dimension):
    """
    Runs a user defined callable to generate the dimension data
    """
    def __init__(self, split_callback, display_callback):
        super(GenericDimension, self).__init__()
        self.split_callback = split_callback
        self.display_callback = display_callback

    def split(self, data):
        return self.split_callback(data)

    def get_display(self, data):
        return self.display_callback(data)