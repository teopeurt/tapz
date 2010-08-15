from tapz.panels.base import Panel
from tapz.panels.dimensions import *
from tapz.panels.intervals import Month, Day, Hour

def _get_dimension_names():
    import inspect
    from tapz.panels import dimensions
    return [name for name, value in dimensions.__dict__.iteritems()
        if inspect.isclass(value) and issubclass(value, dimensions.Dimension)]

__all__ = ['Panel', 'Dimension']
__all__.extend(_get_dimension_names())