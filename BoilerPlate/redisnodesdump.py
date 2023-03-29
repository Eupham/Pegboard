import redis
from redisgraph import Graph

# Connect to Redis
r = redis.Redis(host='localhost', port=6379)

# Create a new RedisGraph instance
g = Graph('mygraph', r)

# Clear all nodes in the graph
g.query("MATCH (n) DELETE n")