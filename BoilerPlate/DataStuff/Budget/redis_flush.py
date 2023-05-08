import redis

class RedisDB:
    def __init__(self, host='localhost', port=6379, db=0):
        self.host = 'localhost'
        self.port = 6379
        self.db = 0
        self.client = redis.StrictRedis(host=host, port=port, db=db)

    def delete_all(self):
        self.client.flushall()
        print("All keys and data have been deleted from Redis.")