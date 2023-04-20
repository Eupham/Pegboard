#EventIO.py

import redis
from ModInit import ModuleInit

modinit = ModuleInit()
#EntityIO.py

import redis
from ModInit import ModuleInit

modinit = ModuleInit()

class EntityIO:
    def __init__(self):
        self.entity_module = modinit.modules[1]

    def add_entity(self, entity_id, name, date_initiated, date_inactive, entity_type, objective_set, party_set, party_role_set, contact_hashes):
        self.entity_module.client.zadd(f"{self.entity_module.name}:metadata:id", {entity_id: 0})
        self.entity_module.client.zadd(f"{self.entity_module.name}:property:name", {name: entity_id})
        self.entity_module.client.zadd(f"{self.entity_module.name}:property:date_initiated", {date_initiated: entity_id})
        self.entity_module.client.zadd(f"{self.entity_module.name}:property:date_inactive", {date_inactive: entity_id})
        self.entity_module.client.zadd(f"{self.entity_module.name}:attribute:type", {entity_type: entity_id})
        self.entity_module.client.zadd(f"{self.entity_module.name}:attribute:objective_set", {objective_set: entity_id})
        self.entity_module.client.zadd(f"{self.entity_module.name}:attribute:party_set", {party_set: entity_id})
        self.entity_module.client.zadd(f"{self.entity_module.name}:attribute:party_role_set", {party_role_set: entity_id})
        self.entity_module.client.zadd(f"{self.entity_module.name}:metadata:contact_hashes", {contact_hashes: entity_id})

    def delete_entity(self, entity_id):
        self.entity_module.client.zrem(f"{self.entity_module.name}:metadata:id", entity_id)
        self.entity_module.client.zrem(f"{self.entity_module.name}:property:name", entity_id)
        self.entity_module.client.zrem(f"{self.entity_module.name}:property:date_initiated", entity_id)
        self.entity_module.client.zrem(f"{self.entity_module.name}:property:date_inactive", entity_id)
        self.entity_module.client.zrem(f"{self.entity_module.name}:attribute:type", entity_id)
        self.entity_module.client.zrem(f"{self.entity_module.name}:attribute:objective_set", entity_id)
        self.entity_module.client.zrem(f"{self.entity_module.name}:attribute:party_set", entity_id)
        self.entity_module.client.zrem(f"{self.entity_module.name}:attribute:party_role_set", entity_id)
        self.entity_module.client.zrem(f"{self.entity_module.name}:metadata:contact_hashes", entity_id)

if __name__ == '__main__':
    entity_io = EntityIO()

    # Adding a new entity
    entity_io.add_entity(
        entity_id=123,
        name="New Entity",
        date_initiated="2023-04-19",
        date_inactive="",
        entity_type="Company",
        objective_set="456",
        party_set="",
        party_role_set="",
        contact_hashes="789"
    )

    # Deleting an entity by id
    entity_id_to_delete = 123
    entity_io.delete_entity(entity_id_to_delete)

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