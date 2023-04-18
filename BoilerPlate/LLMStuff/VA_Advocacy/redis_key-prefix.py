#redis_key-prefix.py
import redis
from typing import Dict

client = redis.Redis('localhost', 6379)

def create_key_prefixes():
    client.setnx("Party_Module", "partymodule")
    client.setnx("Entity_Module", "entitymodule")
    client.setnx("Event_Module", "eventmodule")
    client.setnx("Nash_Module", "nashmodule")
    client.setnx("Integration_Module", "ntegrationmodule")

if __name__ == '__main__':
    create_key_prefixes()