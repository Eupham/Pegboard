import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
redis_client.flushall()

print("All keys and data have been deleted from Redis.")
