from django.test import TestCase
from tapz.panels import Panel, Dimension
from tapz.site import site
from tapz.panels.options import PanelOptions

class TestPanel(Panel):
    pass

class TestPanelWithMeta(Panel):
    class Meta:
        title = 'CoolMetaPanel'
        event_type = 'EV_TYPE'
        routing_key = 'go-here'
        

class TestPanelWithDimensions(Panel):
    dim1 = Dimension()
    dim2 = Dimension()

class TestPanelConstruction(TestCase):
    def test_basic_options(self):
        self.assert_(hasattr(TestPanel, '_meta'))
        self.assert_(isinstance(TestPanel._meta, PanelOptions))
        self.assertEquals(TestPanel._meta.dimensions, {})
        self.assertEquals(TestPanel._meta.title, 'TestPanel')
        self.assertEquals(TestPanel._meta.event_type, 'testpanel')
        self.assertEquals(TestPanel._meta.routing_key, 'tapz.event.%s' % TestPanel._meta.event_type)

    def test_meta_options(self):
        self.assertEquals(TestPanelWithMeta._meta.title, 'CoolMetaPanel')
        self.assertEquals(TestPanelWithMeta._meta.event_type, 'ev_type')
        self.assertEquals(TestPanelWithMeta._meta.routing_key, 'go-here')

    def test_dimensions(self):
        dims = TestPanelWithDimensions._meta.dimensions
        self.assertEquals(len(dims), 2)
        self.assert_('dim1' in dims)
        self.assert_('dim2' in dims)
        self.assertEquals(dims['dim1'].name, 'dim1')
        self.assertEquals(dims['dim2'].name, 'dim2')

