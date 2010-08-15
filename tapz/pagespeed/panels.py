from tapz import panels

class PageSpeedPanel(panels.Panel):
    class Meta:
        title = 'Page Speed'
        event_type = 'pagespeed'

    def call_index(self, request):
        print 'pagespeed'
        return 'pagespeed/index.html', {}