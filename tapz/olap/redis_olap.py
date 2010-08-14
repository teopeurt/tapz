from redis import Redis
import anyjson

"""
Data model in redis:

 EVENT:next_id                  -> auto incrementing integer to be used as ID
 EVENT:ID                       -> individual event detail (hashmap)
 EVENT:dimensions               -> set of dimensions for EVENT
 EVENT:DIM_NAME                 -> set of all top level values for DIM_NAME dimension
 EVENT:DIM_NAME:VALUE           -> set of all event IDs for given EVENT and DIM_NAME VALUE
 EVENT:DIM_NAME:VALUE:subkeys   -> values of all subdimensions
"""

class RedisOlapException(Exception):
    pass

class RedisOlap(object):
    NEXT_ID_KEY = '%s:next_id'
    def __init__(self):
        # TODO: configuration
        self.redis = Redis()

    def register_event(self, event, dimensions):
        """
        Reister an event and store it's dimension set
        """
        pipe = self.redis.pipeline()
        key = '%s:dimensions' % event
        for d in dimensions:
            pipe.sadd(key, d)
        pipe.execute()

    def _get_next_id(self, event):
        """
        Generate and return an ID for given `event`.
        """
        return self.redis.incr(self.NEXT_ID_KEY % event)

    def insert(self, event, data, dimension_map):
        """
        Insert an event instance.
        """
        id = self._get_next_id(event)
        key = '%s:%d' % (event, id)

        pipe = self.redis.pipeline()
        pipe.set(key, anyjson.serialize(data))
        for dimension, values in dimension_map.items():
            # no match for this dimension
            if not values:
                continue

            # add the id to individual dimension buckets
            for v in values:
                pipe.sadd('%s:%s:%s' % (event, dimension, v), id)

            # report dependencies between subbuckets
            top_v = values[0]
            for v in values[1:]:
                pipe.sadd('%s:%s:%s:subkeys' % (event, dimension, top_v), v)
                top_v = v
        pipe.execute()

    def get_data(self, event, **kwargs):
        if not kwargs:
            raise RedisOlapException('You must filter on at least one dimension.')

        valid_dimensions = self.redis.smembers('%s:dimensions' % event)

        keys = []
        for dim, value in kwargs.items():
            # check proper parameters
            if dim not in valid_dimensions:
                raise RedisOlapException('Invalid dimension name %r for event %s.' % (dim, event))

            if not isinstance(value, str):
                raise RedisOlapException('Invalid value for filter %r (must be bytestring).' % dim)
            
            key = '%s:%s:%s' % (event, dim, value)
            # empty ucket, no need to actually query
            if not self.redis.scard(key):
                return

            keys.append(key)

        # TODO: don't mget all at once, do it in chunks
        for e in self.redis.mget(map(lambda k: '%s:%s' % (event, k), self.redis.sinter(keys))):
            yield anyjson.deserialize(e)

