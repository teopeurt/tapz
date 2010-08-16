import time
import sys
from random import choice, randrange

from tapz.site import site

panel = site.get_panel('errors')

line_choices = (10, 11, 17, 326)
time_range = (1270000344, int(time.time()) + 60 * 60 * 24 * 14)
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

site_choices = range(1, 10)

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
    out['site'] = choice(site_choices)
    out['timestamp'] = randrange(*time_range)
    return out


def seed_data(count=10000):
    for x in xrange(count-1):
        if x % 100 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
        data = generate_data()
        panel.add_event(data)
    data = generate_data()
    data['timestamp'] = int(time.time())
    panel.add_event(data)
