#ModInit.py

import redis

client = redis.Redis(host='localhost', port=6379, db=0)

class Plurals:
    def __init__(self, name, parties, entities, events):
        self.name = name
        self.parties = parties
        self.entities = entities
        self.events = events
        self.client = redis.Redis(host='localhost', port=6379, db=0)

    def create_parties_set(self):
        for prop in self.parties:
            self.client.zadd(f"{self.name}:parties:{prop}", {"": 0})

    def create_entities_set(self):
        for attr in self.entities:
            self.client.zadd(f"{self.name}:entities:{attr}", {"": 0})

    def create_events_set(self):
        for meta in self.events:
            self.client.zadd(f"{self.name}:events:{meta}", {"": 0})

class PluralInit:
    PLURALS = {
        "sets": {
            "parties": ["set_id", "id"],
            "entities": ["set_id", "id"],
            "events": ["set_id", "id"]
        }
    }

    def __init__(self):
        self.plurals = []
        for plural_name, plural_data in self.PLURALS.items():
            plural = Plural(plural_name, plural_data["parties"], plural_data["entities"], plural_data["events"])
            self.plurals.append(plural)

    def create_plurals(self):
        for plural in self.plurals:
            plural.create_parties_set()
            plural.create_entities_set()
            plural.create_events_set()


class Module:
    def __init__(self, name, properties, attributes, metadata):
        self.name = name
        self.properties = properties
        self.attributes = attributes
        self.metadata = metadata
        self.client = redis.Redis(host='localhost', port=6379, db=0)

    def create_properties(self):
        for prop in self.properties:
            self.client.zadd(f"{self.name}:property:{prop}", {"": 0})

    def create_attributes(self):
        for attr in self.attributes:
            self.client.zadd(f"{self.name}:attribute:{attr}", {"": 0})

    def create_metadata(self):
        for meta in self.metadata:
            self.client.zadd(f"{self.name}:metadata:{meta}", {"": 0})

class ModuleInit:
    MODULES = {
        "party": {
            "properties": ["name", "date_formed", "date_disbanded"],
            "attributes": ["type", "entity_set","event_set", "objective_set", "action_set"],
            "metadata": ["id", "description", ""]
        },
        "entity": {
            "properties": ["name", "date_initiated", "date_inactive"],
            "attributes": ["type", "objective_set", "party_set", "party_role_set"],
            "metadata": ["id", "description", "contact_hashes"]
        },
        "event": {
            "properties": ["name", "location", "datetime_start", "datetime_end"],
            "attributes": ["type", "party_set", "result_set"],
            "metadata": ["id", "description"]
        },
        "nash": {
            "properties": ["name"],
            "attributes": ["event_set", "interest_weight_set","payoff_set"],
            "metadata": ["id"]
        }
    }

    def __init__(self):
        self.modules = []
        for module_name, module_data in self.MODULES.items():
            module = Module(module_name, module_data["properties"], module_data["attributes"], module_data["metadata"])
            self.modules.append(module)

    def create_modules(self):
        for module in self.modules:
            module.create_properties()
            module.create_attributes()
            module.create_metadata()

if __name__ == '__main__':
    modinit = ModuleInit()
    modinit.create_modules()

    # Adding a new entity to the "entity" module
    entity_id = 123
    entity_name = "New Entity"
    entity_date_initiated = "2023-04-19"
    entity_date_inactive = ""
    entity_type = "Company"
    entity_objective_set = "456"
    entity_party_set = ""
    entity_party_role_set = ""
    entity_contact_hashes = "789"

    entity_module = modinit.modules[1]  # Get the "entity" module
    entity_module.client.zadd(f"{entity_module.name}:metadata:id", {entity_id: 0})
    entity_module.client.zadd(f"{entity_module.name}:property:name", {entity_name: entity_id})
    entity_module.client.zadd(f"{entity_module.name}:property:date_initiated", {entity_date_initiated: entity_id})
    entity_module.client.zadd(f"{entity_module.name}:property:date_inactive", {entity_date_inactive: entity_id})
    entity_module.client.zadd(f"{entity_module.name}:attribute:type", {entity_type: entity_id})
    entity_module.client.zadd(f"{entity_module.name}:attribute:objective_set", {entity_objective_set: entity_id})
    entity_module.client.zadd(f"{entity_module.name}:attribute:party_set", {entity_party_set: entity_id})
    entity_module.client.zadd(f"{entity_module.name}:attribute:party_role_set", {entity_party_role_set: entity_id})
    entity_module.client.zadd(f"{entity_module.name}:metadata:contact_hashes", {entity_contact_hashes: entity_id})

    # # Deleting the entity using its ID
    # entity_module.client.zrem(f"{entity_module.name}:metadata:id", entity_id)
    # entity_module.client.zrem(f"{entity_module.name}:property:name", entity_name)
    # entity_module.client.zrem(f"{entity_module.name}:property:date_initiated", entity_date_initiated)
    # entity_module.client.zrem(f"{entity_module.name}:property:date_inactive", entity_date_inactive)
    # entity_module.client.zrem(f"{entity_module.name}:attribute:type", entity_type)
    # entity_module.client.zrem(f"{entity_module.name}:attribute:objective_set", entity_objective_set)
    # entity_module.client.zrem(f"{entity_module.name}:attribute:party_set", entity_party_set)
    # entity_module.client.zrem(f"{entity_module.name}:attribute:party_role_set", entity_party_role_set)
    # entity_module.client.zrem(f"{entity_module.name}:metadata:contact_hashes", entity_contact_hashes)
