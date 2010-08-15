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

class TestRegistry(TestCase):
    def setUp(self):
        site._auto_discover()
        self._registry_backup = site.__class__._panels
        site.__class__._panels = {}
        site.register(TestPanel)
        site.register(TestPanelWithMeta)
        site.register(TestPanelWithDimensions)

    def tearDown(self):
        site.__class__._panels = self._registry_backup

    def test_get_panel_by_type(self):
        self.assert_(isinstance(site.get_panel('testpanel'), TestPanel))
        self.assert_(isinstance(site.get_panel('ev_type'), TestPanelWithMeta))

    def test_get_all_panels(self):
        panels = site.get_panels()
        self.assertEquals(len(panels), 3)
        # panels is sorted by panel title -- order matters with these
        for i, panel in enumerate((TestPanelWithMeta, TestPanel, TestPanelWithDimensions)):
            data = panels[i]
            self.assertEquals(panel._meta.title, data['title'])
            self.assertEquals(panel._meta.event_type, data['type'])
