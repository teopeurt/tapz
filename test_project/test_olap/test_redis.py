from test_project.helpers import RedisTestCase

from tapz.olap.redis_olap import RedisOlap

class RedisOlapTestCase(RedisTestCase):
    def setUp(self):
        super(RedisOlapTestCase, self).setUp()
        self.olap = RedisOlap()

        # inject our own redis client
        self.olap.redis = self.redis

class TestEventCreation(RedisOlapTestCase):
    def test_register_event_creates_event_dimensions_in_redis(self):
        self.olap.register_event('event_name', ['time', 'other_dimension'])
        self.assertEquals(set(['time', 'other_dimension']), self.redis.smembers('event_name:dimensions'))

class TestEventInsertion(RedisOlapTestCase):
    def test_event_stored_in_full(self):
        self.olap.insert('error', {'some': 42, 'complex': 'data'}, {})
        self.assertEquals({'some': '42', 'complex': 'data'}, self.redis.hgetall('error:1'))

    def test_event_registered_in_dimension_buckets(self):
        self.olap.insert('error', {'some': 'details'}, {'time': ['2010', '201008', '20100810'], 'name': ['ValueError']})
        for k in ('error:time:2010', 'error:time:201008', 'error:time:20100810', 'error:name:ValueError'):
            self.assertEquals(set(['1']), self.redis.smembers(k))
    
    def test_dimension_rependencies_get_registered_on_insert(self):
        self.olap.insert('error', {'some': 'details'}, {'time': ['2010', '201008', '20100810'], 'name': ['ValueError']})
        self.assertEquals(set(['201008']), self.redis.smembers('error:time:2010:subkeys'))
        self.assertEquals(set(['20100810']), self.redis.smembers('error:time:201008:subkeys'))
        assert not self.redis.exists('error:name:ValueError:subkeys')
