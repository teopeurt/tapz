import datetime
import time
from django.test import TestCase

from tapz.panels.intervals import Month, Day, Hour

_test_datetime = datetime.datetime(2010, 8, 14, 15, 13, 12)

class TestIntervals(TestCase):
    def test_month_pack(self):
        self.assertEquals(Month.pack(_test_datetime), "201008")

    def test_month_unpack(self):
        self.assertEquals(Month.unpack("201008"), datetime.datetime(2010, 8, 1))

    def test_day_pack(self):
        self.assertEquals(Day.pack(_test_datetime), "20100814")

    def test_day_unpack(self):
        self.assertEquals(Day.unpack("20100814"), datetime.datetime(2010, 8, 14))

    def test_hour_pack(self):
        self.assertEquals(Hour.pack(_test_datetime), "2010081415")

    def test_hour_unpack(self):
        self.assertEquals(Hour.unpack("2010081415"), datetime.datetime(2010, 8, 14, 15))
