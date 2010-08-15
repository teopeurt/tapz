from datetime import datetime
import time
from django.test import TestCase

from tapz.panels.intervals import Month, Day, Hour

_test_datetime = datetime(2010, 8, 14, 15, 13, 12)

class TestIntervals(TestCase):
    def _test_range(self, interval, start, end, expected):
        rng = interval.range(start, end)
        found = [interval.pack(i) for i in rng]
        self.assertEquals(expected, found)

    def test_month_pack(self):
        self.assertEquals(Month.pack(_test_datetime), "201008")

    def test_month_unpack(self):
        self.assertEquals(Month.unpack("201008"), datetime(2010, 8, 1))

    def test_month_range(self):
        self._test_range(
            Month,
            datetime(2010, 6, 14),
            datetime(2010, 8, 13),
            ['201006', '201007', '201008']
            )
        self._test_range(
            Month,
            datetime(2010, 6, 14),
            datetime(2010, 8, 20),
            ['201006', '201007', '201008']
            )
        # month does special logic when spanning years
        self._test_range(
            Month,
            datetime(2008, 11, 1),
            datetime(2010, 2, 1),
            ['200811','200812','200901','200902','200903','200904','200905',
             '200906','200907','200908','200909','200910','200911','200912',
             '201001','201002',
            ])

    def test_day_pack(self):
        self.assertEquals(Day.pack(_test_datetime), "20100814")

    def test_day_unpack(self):
        self.assertEquals(Day.unpack("20100814"), datetime(2010, 8, 14))

    def test_day_range(self):
        self._test_range(
            Day,
            datetime(2010, 7, 28),
            datetime(2010, 8, 2),
            ['20100728','20100729','20100730','20100731','20100801','20100802']
            )

    def test_hour_pack(self):
        self.assertEquals(Hour.pack(_test_datetime), "2010081415")

    def test_hour_unpack(self):
        self.assertEquals(Hour.unpack("2010081415"), datetime(2010, 8, 14, 15))

    def test_hour_range(self):
        self._test_range(
            Hour,
            datetime(2010, 8, 14, 22, 1),
            datetime(2010, 8, 15, 2, 8),
            ['2010081422','2010081423','2010081500','2010081501','2010081502']
            )
