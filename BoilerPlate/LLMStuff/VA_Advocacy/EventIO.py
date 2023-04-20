#EventIO.py

import redis
from ModInit import ModuleInit

modinit = ModuleInit()

class EventIO:
    def __init__(self):
        self.event_module = modinit.modules[2]

    def add_event(self, event_id, name, location, datetime_start, datetime_end, event_type, party_set, result_set, description):
        self.event_module.client.zadd(f"{self.event_module.name}:metadata:id", {event_id: 0})
        self.event_module.client.zadd(f"{self.event_module.name}:property:name", {name: event_id})
        self.event_module.client.zadd(f"{self.event_module.name}:property:location", {location: event_id})
        self.event_module.client.zadd(f"{self.event_module.name}:property:datetime_start", {datetime_start: event_id})
        self.event_module.client.zadd(f"{self.event_module.name}:property:datetime_end", {datetime_end: event_id})
        self.event_module.client.zadd(f"{self.event_module.name}:attribute:type", {event_type: event_id})
        self.event_module.client.zadd(f"{self.event_module.name}:attribute:party_set", {party_set: event_id})
        self.event_module.client.zadd(f"{self.event_module.name}:attribute:result_set", {result_set: event_id})
        self.event_module.client.zadd(f"{self.event_module.name}:metadata:description", {description: event_id})

    def delete_event(self, event_id):
        self.event_module.client.zrem(f"{self.event_module.name}:metadata:id", event_id)
        self.event_module.client.zremrangebyscore(f"{self.event_module.name}:property:name", event_id, event_id)
        self.event_module.client.zremrangebyscore(f"{self.event_module.name}:property:location", event_id, event_id)
        self.event_module.client.zremrangebyscore(f"{self.event_module.name}:property:datetime_start", event_id, event_id)
        self.event_module.client.zremrangebyscore(f"{self.event_module.name}:property:datetime_end", event_id, event_id)
        self.event_module.client.zremrangebyscore(f"{self.event_module.name}:attribute:type", event_id, event_id)
        self.event_module.client.zremrangebyscore(f"{self.event_module.name}:attribute:party_set", event_id, event_id)
        self.event_module.client.zremrangebyscore(f"{self.event_module.name}:attribute:result_set", event_id, event_id)
        self.event_module.client.zremrangebyscore(f"{self.event_module.name}:metadata:description", event_id, event_id)

if __name__ == '__main__':
    event_io = EventIO()

    # Add an event
    event_io.add_event(1, "New Year's Party", "123 Main St", "2023-12-31T20:00:00", "2024-01-01T02:00:00", "Party", "1,2", "1,2,3", "A fun party to ring in the new year!")
    print("Event added")

    # Delete an event
    event_io.delete_event(1)
    print("Event deleted")