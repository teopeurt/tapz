from redis import Redis

"""
Data model in redis:

 EVENT:next_id                  -> auto incrementing integer to be used as ID
 EVENT:ID                       -> individual event detail (hashmap)
 EVENT:dimensions               -> set of dimensions for EVENT
 EVENT:DIM_NAME                 -> set of all top level values for DIM_NAME dimension
 EVENT:DIM_NAME:VALUE           -> set of all event IDs for given EVENT and DIM_NAME VALUE
 EVENT:DIM_NAME:VALUE:subkeys   -> values of all subdimensions
"""

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
        pipe.hmset(key, data)
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



