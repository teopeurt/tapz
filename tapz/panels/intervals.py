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
        return value.strftime(cls.pack_format_string)

    @classmethod
    def unpack(cls, value):
        """
        Unpack a string into a datetime object
        """
        return datetime.datetime.strptime(value, cls.pack_format_string)

    @classmethod
    def display_format(cls, rng):
        return [d.strftime(cls.display_format_string) for d in rng]

    @classmethod
    def pack_format(cls, rng):
        return [d.strftime(cls.pack_format_string) for d in rng]

class Hour(Interval):
    display_name = 'Hour'
    divides_into = None
    pack_format_string = '%Y%m%d%H'
    delta = datetime.timedelta(hours=1)
    display_format_string = "%H"

class Day(Interval):
    display_name = 'Day'
    divides_into = Hour
    pack_format_string = '%Y%m%d'
    delta = datetime.timedelta(days=1)
    display_format_string = "%m-%d-%y"

class Month(Interval):
    display_name = 'Month'
    divides_into = Day
    pack_format_string = '%Y%m'
    display_format_string = "%M %y"

    @classmethod
    def range(cls, start, end):
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

