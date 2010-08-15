import anyjson

from test_project.helpers import RedisTestCase

from tapz.olap.redis_olap import RedisOlap, RedisOlapException

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
        self.assertEquals(anyjson.serialize({'some': 42, 'complex': 'data'}), self.redis.get('error:1'))

    def test_event_registered_in_dimension_buckets(self):
        self.olap.insert('error', {'some': 'details'}, {'time': ['2010', '201008', '20100810'], 'name': ['ValueError']})
        for k in ('error:time:2010', 'error:time:201008', 'error:time:20100810', 'error:name:ValueError'):
            self.assertEquals(set(['1']), self.redis.smembers(k))
    
    def test_dimension_rependencies_get_registered_on_insert(self):
        self.olap.insert('error', {'some': 'details'}, {'time': ['2010', '201008', '20100810'], 'name': ['ValueError']})
        self.assertEquals(set(['201008']), self.redis.smembers('error:time:2010:subkeys'))
        self.assertEquals(set(['20100810']), self.redis.smembers('error:time:201008:subkeys'))
        assert not self.redis.exists('error:name:ValueError:subkeys')

class TestDataRetrieval(RedisOlapTestCase):
    def test_get_keys_stops_on_invalid_dimension(self):
        self.assertRaises(RedisOlapException, self.olap.get_keys, 'error', time='201008')

    def test_get_keys_stops_on_invalid_dimension_value(self): 
        self.redis.sadd('error:dimensions', 'time')
        self.assertRaises(RedisOlapException, self.olap.get_keys, 'error', time=201008)

    def test_get_keys_returns_empty_if_one_bucket_is_empty(self):
        self.redis.sadd('error:dimensions', 'time')
        self.redis.sadd('error:dimensions', 'name')
        self.redis.sadd('error:time:201008', '1')
        self.assertEquals(0, len(list(self.olap.get_keys('error', time='201008', name='ValueError'))))

    def test_get_instances_returns_correct_data(self):
        self.redis.sadd('error:dimensions', 'time')
        self.redis.sadd('error:dimensions', 'name')
        self.redis.sadd('error:time:201008', '1')
        self.redis.sadd('error:time:201008', '2')
        self.redis.sadd('error:time:201008', '3')
        self.redis.sadd('error:name:ValueError', '1')
        self.redis.sadd('error:name:ValueError', '3')
        self.redis.sadd('error:name:ValueError', '4')
        for x in ('1', '2', '3', '4'):
            self.redis.set('error:%s' % x, anyjson.serialize({'event': 'error:%s' % x}))

        values = set(map(anyjson.serialize, self.olap.get_instances('error', time='201008', name='ValueError')))
        self.assertEquals(2, len(values))
        self.assertEquals(set([anyjson.serialize({'event': 'error:1'}), anyjson.serialize({'event': 'error:3'})]), values)


    def test_get_instances_can_union_more_than_one_slice_from_each_dimension(self):
        self.redis.sadd('error:dimensions', 'time')
        self.redis.sadd('error:dimensions', 'name')
        self.redis.sadd('error:time:201008', '1')
        self.redis.sadd('error:time:201008', '2')
        self.redis.sadd('error:time:201009', '3')
        self.redis.sadd('error:name:ValueError', '1')
        self.redis.sadd('error:name:ValueError', '3')
        self.redis.sadd('error:name:ValueError', '4')
        for x in ('1', '2', '3', '4'):
            self.redis.set('error:%s' % x, anyjson.serialize({'event': 'error:%s' % x}))

        values = set(map(anyjson.serialize, self.olap.get_instances('error', time=('201008', '201009'), name='ValueError')))
        self.assertEquals(2, len(values))
        self.assertEquals(set([anyjson.serialize({'event': 'error:1'}), anyjson.serialize({'event': 'error:3'})]), values)


