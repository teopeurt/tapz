from django.core.urlresolvers import reverse

from test_project.helpers import DjangoRedisTestCase

class TestErrorPanelMiddleware(DjangoRedisTestCase):
    def test_status_500_is_returned(self):
        resp = self.client.get(reverse('test-fail-horribly'))
        self.assertEquals(500, resp.status_code)

