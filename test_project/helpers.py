from unittest import TestCase
import nose

from redis import Redis

class RedisTestCase(TestCase):
    def setUp(self):
        super(RedisTestCase, self).setUp()
        self.redis = Redis()
        try:
            if not self.redis.ping():
                raise nose.SkipTest()
        except:
            raise nose.SkipTest()

    def tearDown(self):
        super(RedisTestCase, self).tearDown()
        self.redis.flushdb()


