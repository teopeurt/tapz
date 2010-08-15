from tapz import panels

class ErrorPanel(panels.Panel):
    timestamp = panels.DateTimeDimension()
    site = panels.SiteDimension()

    class Meta:
        event_type = 'errors'
        title = 'Errors'
