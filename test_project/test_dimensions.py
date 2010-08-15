import datetime
import time
from django.test import TestCase
from django.contrib.sites.models import Site

from tapz.panels.dimensions import DateTimeDimension, SiteDimension
from tapz.panels.intervals import Month, Day, Hour

class TestDateTimeDimension(TestCase):
    def test_display(self):
        dim = DateTimeDimension()
        self.assertEquals(dim.get_display("2010081415", Hour),
                          datetime.datetime(2010, 8, 14, 15))
        self.assertEquals(dim.get_display("20100814", Day),
                          datetime.datetime(2010, 8, 14))
        self.assertEquals(dim.get_display("201008", Month),
                          datetime.datetime(2010, 8, 1))

    def test_split(self):
        dim = DateTimeDimension()
        parts = dim.split("1281833013") #2010, 8, 14, 19
        self.assertEquals(parts[0], "201008")
        self.assertEquals(parts[1], "20100814")
        self.assertEquals(parts[2], "2010081419")

class TestSiteDimension(TestCase):
    def test_display(self):
        dim = SiteDimension()
        self.assertEquals(dim.get_display(1), Site.objects.get_current().domain)
