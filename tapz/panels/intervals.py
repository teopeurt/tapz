import datetime

class Interval(object):
    "Base date interval class"
    @classmethod
    def range(cls, start, end):
        """
        Return a range of datetime objects between start and end
        """
        r = []
        while start <= end:
            r.append(start)
            start += cls.delta
        return r

    @classmethod
    def pack(cls, value):
        """
        Pack a datetime object into a string
        """
        return value.strftime(cls.format_string)

    @classmethod
    def unpack(cls, value):
        """
        Unpack a string into a datetime object
        """
        return datetime.datetime.strptime(value, cls.format_string)

class Month(Interval):
    format_string = '%Y%m'

    def range(self, start, end):
        # there's no "months" arg for timedelta.
        r = []
        # reset the start date to the beginning of the month
        start = datetime.datetime(year=start.year, month=start.month, day=1)
        while start <= end:
            r.append(start)
            if start.month == 12:
                start = datetime.datetime(year=start.year+1, month=1, day=1)
            else:
                start = datetime.datetime(year=start.year, month=start.month+1, day=1)
        return r

class Day(Interval):
    format_string = '%Y%m%d'
    delta = datetime.timedelta(days=1)

class Hour(Interval):
    format_string = '%Y%m%d%H'
    delta = datetime.timedelta(hours=1)
