import anyjson

from django.core.urlresolvers import reverse

from test_project.helpers import DjangoRedisTestCase
from test_project import test_template_loader

class TestErrorPanelMiddleware(DjangoRedisTestCase):
    def test_status_500_is_returned(self):
        test_template_loader.templates['500.html'] = '500'
        resp = self.client.get(reverse('test-fail-horribly'))
        self.assertEquals(500, resp.status_code)

    def test_correct_data_is_stpored_in_redis(self):
        test_template_loader.templates['500.html'] = '500'
        resp = self.client.get(reverse('test-fail-horribly'))

        exc_data = anyjson.deserialize(self.redis.get('errors:1'))
        self.assertEquals(11, exc_data['line_number'])
        self.assertEquals('MyException', exc_data['exc_name'])

