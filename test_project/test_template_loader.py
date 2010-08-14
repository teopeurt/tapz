from unittest import TestCase

from django.template import TemplateDoesNotExist 


templates = {}

def load_template_source(template_name, dirs=None):
    "Dummy template loader that returns templates from local templates dictionary."
    try:
        return templates.pop(template_name), template_name
    except KeyError, e:
        raise TemplateDoesNotExist(e)
load_template_source.is_usable = True

class TestDummyTemplateLoader(TestCase):
    def tearDown(self):
        global templates
        templates = {}

    def test_simple(self):
        templates['anything.html'] = 'Something'
        source, name = load_template_source('anything.html')
        self.assertEquals('anything.html', name)
        self.assertEquals('Something', source)

    def test_empty(self):
        self.assertRaises(TemplateDoesNotExist, load_template_source, 'anything.html')

