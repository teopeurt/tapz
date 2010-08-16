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

    def __init__(self, **kwargs):
        self.redis = Redis(**kwargs)

    def register_event(self, event, dimensions):
        """
        Reister an event and store it's dimension set
        """
        pipe = self.redis.pipeline()
        key = '%s:dimensions' % event
        for d in dimensions:
            pipe.sadd(key, d)
        pipe.execute()

    def get_dimension_values(self, event, dimension, super_value=None):
        if super_value:
            key = '%s:%s:%s' % (event, dimension, super_value)
        else:
            key = '%s:%s' % (event, dimension)
        return self.redis.smembers(key)

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

        data['id'] = id
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

    def get_last_instance(self, event):
        id = self.redis.get(self.NEXT_ID_KEY % event)
        if not id:
            return None
        return anyjson.deserialize(self.redis.get('%s:%s' % (event, id)))

    def get_keys(self, event, **kwargs):
        if not kwargs:
            raise RedisOlapException('You must filter on at least one dimension.')

        valid_dimensions = self.redis.smembers('%s:dimensions' % event)

        keys = []
        for dim, value in kwargs.items():
            operation = None

            # specific operation requested
            if '__' in dim:
                dim, operation = dim.split('__', 1)

            # check proper parameters
            if dim not in valid_dimensions:
                raise RedisOlapException('Invalid dimension name %r for event %s.' % (dim, event))

            # more sliced wanted, we have to union those
            if isinstance(value, (tuple, list)):
                for v in value:
                    if not isinstance(v, str):
                        raise RedisOlapException('Invalid value for filter %r (must be bytestring).' % dim)

                # no operation or operatin is intersect, leave this for the final merging
                if not operation or operation == 'intersect':
                    keys.extend(value)
                    continue

                elif operation:
                    if operation not in ('union', 'diff'):
                        raise RedisOlapException('Invalid opeartion %r.' % operation)
                    
                    key = '%s:%s:%s' % (event, operation, ','.join(value))
                    keys_to_merge = map(lambda value: '%s:%s:%s' % (event, dim, value), value)

                    if operation == 'union':
                        self.redis.sunionstore(key, keys_to_merge)
                    else:
                        self.redis.sdiffstore(key, keys_to_merge)

                    self.redis.expire(key, 10)

            elif not isinstance(value, str):
                raise RedisOlapException('Invalid value for filter %r (must be bytestring).' % dim)
            elif operation:
                # operation requested but only one value given
                raise RedisOlapException('Invalid operation for value %r (must be list or tuple).' % value)
            else:
                key = '%s:%s:%s' % (event, dim, value)
            
            keys.append(key)

        return keys

    def get_instances(self, keys):
        """
        Retrieve set of keys from redis.
        """
        if not keys:
            return

        # TODO: don't mget all at once, do it in chunks
        for e in self.redis.mget(keys):
            yield anyjson.deserialize(e)

    def compute_aggregation(self, event, aggregation, keys):
        """
        Given a final list of keys for a given cell in resulting grid. Compute
        the aggregation.
        """
        if not aggregation:
            key = '%s:sinterstore:%s' % (event, ','.join(keys))
            self.redis.sinterstore(key, keys)
            self.redis.expire(key, 10)
            return self.redis.scard(key)
        ids = self.redis.sinter(keys)

        return aggregation(self.get_instances(map(lambda k: '%s:%s' % (event, k), ids)))

    def aggregate(self, event, aggregation=None, filters=None, rows=None, columns=None):
        """
        Main top-level method used for accessing the data in OLAP.

        Paramaters::

            `event`:        name of the event
            `aggregation`:  function that accepts and iterator of instances and returns result
            `filters`:      dictionary containing global filters
            `rows`:         list of dictionaries with filters defining individual rows
            `columns`:      list of dictionaries with filters defining individual columns

        Example::
            olap.aggregate(
                'page_views',
                aggregation=SUM,
                filters={'content_type': VIDEO},
                rows=[{'time': 2009}, {'time__union': [201001, 201002, 201003,]},],
                columns=[{'logged_in': True}, {'logged_in': False}]
            )
        """
        if not rows:
            raise RedisOlapException('You must specify at least on row when aggregating.')

        columns = columns or []

        row_keys = [self.get_keys(event, **row) for row in rows]
        column_keys = [self.get_keys(event, **column) for column in columns]
        if filters:
            filter_keys = self.get_keys(event, **filters)
        else:
            filter_keys = []

        # TODO: paralel execution?
        for r in row_keys:
            if column_keys:
                row = []
                for c in column_keys:
                    row.append(self.compute_aggregation(event, aggregation, filter_keys + r + c))
            else:
                row = append(self.compute_aggregation(event, aggregation, filter_keys + r))
            yield row

