from unittest import TestCase as UnitTestCase
import nose

from django.test import TestCase as DjangoTestCase

from redis import Redis

class RedisTestCaseMixin(object):
    def setUp(self):
        super(RedisTestCaseMixin, self).setUp()
        self.redis = Redis()
        try:
            if not self.redis.ping():
                raise nose.SkipTest()
        except:
            raise nose.SkipTest()

    def tearDown(self):
        super(RedisTestCaseMixin, self).tearDown()
        self.redis.flushdb()


class RedisTestCase(RedisTestCaseMixin, UnitTestCase):
    pass

class DjangoRedisTestCase(RedisTestCaseMixin, DjangoTestCase):
    pass

