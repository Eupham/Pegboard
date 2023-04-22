#ActionIO.py

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
