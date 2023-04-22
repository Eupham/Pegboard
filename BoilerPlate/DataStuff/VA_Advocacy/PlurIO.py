#PlurIO.py

import redis

class PluralIO:
    def __init__(self, name):
        self.name = name
        self.client = redis.Redis(host='localhost', port=6379, db=0)

    def add(self, plural_type, plural_id, score):
        key = f"{self.name}:{plural_type}:{plural_id}"
        self.client.zadd(key, {score: plural_id})

    def delete(self, plural_type, plural_id):
        key = f"{self.name}:{plural_type}:{plural_id}"
        self.client.delete(key)

if __name__ == '__main__':
    plural_io = PluralIO("sets")
    plural_io.add("parties", 123, 1)

    plural_io.delete("parties", 123)