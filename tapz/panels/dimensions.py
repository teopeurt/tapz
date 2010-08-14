class Dimension(object):
    def __init__(self):
        self.name = None

    def contribute_to_class(self, cls, name):
        cls._meta.dimensions[name] = self

    def get_display(self, value):
        return value

    def split(self, value):
        return [value]
