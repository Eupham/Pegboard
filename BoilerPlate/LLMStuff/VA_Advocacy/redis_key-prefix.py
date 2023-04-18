import redis
from typing import Dict

# Create connections to Redis instances (assuming you have them configured)
client = redis.Redis('localhost', 6379)
event_bus = redis.Redis('localhost', 6379)

def create_key_prefixes():
    client.setnx("Party_Module", "partymodule")
    event_bus.setnx("Event_Module", "eventmodule")
    # Add more key prefix creation lines below

if __name__ == '__main__':
    create_key_prefixes()