from django.test import TestCase
from django.http import HttpResponse
from tapz.panels import Panel
from tapz.exceptions import PanelMethodDoesNotExist

class FakeRequest(object):
    def __init__(self):
        self.GET = {}
        self.COOKIES = {}
        self.POST = {}

class ContextTestPanel(Panel):
    def get_filters(self, request):
        return {}

    def call_index(self, request, context, **filters):
        r = HttpResponse('')
        r._name = 'index'
        return r

    def call_bar(self, request, context, **filters):
        r = HttpResponse('')
        r._name = 'bar'
        return r

    def call_pending_cookies(self, request, context, **filters):
        self.add_cookie(request, 'foo', 'bar')
        return HttpResponse('')

class TestPanelContext(TestCase):
    def test_invalid_subcall(self):
        p = ContextTestPanel()
        self.assertRaises(PanelMethodDoesNotExist, p.get_response, None, 'foo')

    def test_no_subcall(self):
        p = ContextTestPanel()
        r = FakeRequest()
        response = p.get_response(r, None)
        self.assertEquals(response._name, 'index')
    
    def test_subcall(self):
        p = ContextTestPanel()
        r = FakeRequest()
        response = p.get_response(r, 'bar')
        self.assertEquals(response._name, 'bar')

    def test_no_cookies(self):
        p = ContextTestPanel()
        r = FakeRequest()
        response = p.get_response(r)
        self.assertEquals(len(response.cookies), 0)

    def test_cookies(self):
        p = ContextTestPanel()
        r = FakeRequest()
        response = p.get_response(r, 'pending_cookies')
        self.assertEquals(len(response.cookies), 1)
        self.assert_('foo' in response.cookies)
