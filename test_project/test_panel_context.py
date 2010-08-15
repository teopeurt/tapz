from django.test import TestCase
from tapz.panels import Panel
from tapz.exceptions import PanelMethodDoesNotExist

class ContextTestPanel(Panel):
    def call_index(self, request):
        return 'foo/index.html', {}

    def call_bar(self, request):
        return 'bar/index.html', {}

class TestPanelContext(TestCase):
    def test_invalid_subcall(self):
        p = ContextTestPanel()
        self.assertRaises(PanelMethodDoesNotExist, p.get_context, None, 'foo')

    def test_no_subcall(self):
        p = ContextTestPanel()
        tpl, context = p.get_context(None, None)
        self.assertEquals(tpl, 'foo/index.html', {})
        self.assert_('current_panel' in context)
        self.assert_('panels' in context)

    def test_subcall(self):
        p = ContextTestPanel()
        tpl, context = p.get_context(None, 'bar')
        self.assertEquals(tpl, 'bar/index.html', {})


