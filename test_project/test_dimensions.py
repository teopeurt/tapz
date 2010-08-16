import datetime
import time
from django.test import TestCase
from django.db import models
from django.contrib.sites.models import Site

from tapz.panels.dimensions import (DateTimeDimension, SiteDimension,
                                    RelatedObjectDimension, GenericDimension)
from tapz.panels.intervals import Month, Day, Hour

class FooModel(models.Model):
    name = models.CharField(max_length=40)

class TestDateTimeDimension(TestCase):
    def test_display(self):
        dim = DateTimeDimension()
        dim.name = 'foo'
        self.assertEquals(dim.get_display({'foo': "2010081415"}, Hour),
                          datetime.datetime(2010, 8, 14, 15))
        self.assertEquals(dim.get_display({'foo': "20100814"}, Day),
                          datetime.datetime(2010, 8, 14))
        self.assertEquals(dim.get_display({'foo': "201008"}, Month),
                          datetime.datetime(2010, 8, 1))

    def test_split(self):
        dim = DateTimeDimension()
        dim.name = 'foo'
        parts = dim.split({'foo': "1281833013"}) #2010, 8, 14, 19
        self.assertEquals(parts[0], "201008")
        self.assertEquals(parts[1], "20100814")
        self.assertEquals(parts[2], "2010081419")

class TestSiteDimension(TestCase):
    def test_display(self):
        dim = SiteDimension()
        dim.name = 'foo'
        self.assertEquals(dim.get_display({'foo': 1}), Site.objects.get_current().domain)

# class TestRelatedObjectDimension(TestCase):
#     def test_split(self):
#         dim = RelatedObjectDimension(FooModel, 'name')
#         f = FooModel.objects.create()
#         self.assertEquals(dim.split(f), [f.id])
# 
#     def test_display(self):
#         dim = RelatedObjectDimension(FooModel, 'name')
#         f = FooModel.objects.create(name='foobar')
#         self.assertEquals(dim.get_display(f.id), 'foobar')
