import sys
from random import choice, randrange

from tapz.site import site

panel = site.get_panel('errors')

line_choices = (10, 11, 17, 326)
time_range = (1270000344, 1281828344)
url_choices = (
    'http://testserver/fail/',
    'http://testserver/come/other/ur/',
    'http://other_server.com/',
)
name_choices = (
    'ValueError', 'TypeError', 'CategoryDoesNotExist', 'KeyError', 'Exception', 'NotImplementedHere', 'NotImplementedHere'
)
module_choices = (
    'tapz.views', 'django.contrib.views.list', 'eat.carrot.and.die', 'empire.strikes.back'
)

default_data = {
    "line_number": 11,
    "exc_name": "MyException",
    "url": "http://testserver/fail/",
    "timestamp": 1281820344.78,
    "module": "",
    "exc_value": "XXX"
}

def generate_data():
    out= default_data.copy()
    out['line_number'] = choice(line_choices)
    out['exc_name'] = choice(name_choices)
    out['url'] = choice(url_choices)
    out['module'] = choice(module_choices)
    out['timestamp'] = randrange(*time_range)
    return out


def seed_data(count=10000):
    for x in xrange(count):
        if x % 10 == 0:
            sys.stdout.write('.')
        data = generate_data()
        panel.add_event(data)
