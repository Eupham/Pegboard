#PartyIO.py

import redis
from ModInit import ModuleInit

modinit = ModuleInit()

class PartyIO:
    def __init__(self):
        self.party_module = modinit.modules[0]

    def add_party(self, party_id, name, date_formed, date_disbanded, party_type, entity_set, event_set, objective_set, action_set):
        self.party_module.client.zadd(f"{self.party_module.name}:metadata:id", {party_id: 0})
        self.party_module.client.zadd(f"{self.party_module.name}:property:name", {name: party_id})
        self.party_module.client.zadd(f"{self.party_module.name}:property:date_formed", {date_formed: party_id})
        self.party_module.client.zadd(f"{self.party_module.name}:property:date_disbanded", {date_disbanded: party_id})
        self.party_module.client.zadd(f"{self.party_module.name}:attribute:type", {party_type: party_id})
        self.party_module.client.zadd(f"{self.party_module.name}:attribute:entity_set", {entity_set: party_id})
        self.party_module.client.zadd(f"{self.party_module.name}:attribute:event_set", {event_set: party_id})
        self.party_module.client.zadd(f"{self.party_module.name}:attribute:objective_set", {objective_set: party_id})
        self.party_module.client.zadd(f"{self.party_module.name}:attribute:action_set", {action_set: party_id})

    def delete_party(self, party_id):
        self.party_module.client.zrem(f"{self.party_module.name}:metadata:id", party_id)
        self.party_module.client.zrem(f"{self.party_module.name}:property:name", party_id)
        self.party_module.client.zrem(f"{self.party_module.name}:property:date_formed", party_id)
        self.party_module.client.zrem(f"{self.party_module.name}:property:date_disbanded", party_id)
        self.party_module.client.zrem(f"{self.party_module.name}:attribute:type", party_id)
        self.party_module.client.zrem(f"{self.party_module.name}:attribute:entity_set", party_id)
        self.party_module.client.zrem(f"{self.party_module.name}:attribute:event_set", party_id)
        self.party_module.client.zrem(f"{self.party_module.name}:attribute:objective_set", party_id)
        self.party_module.client.zrem(f"{self.party_module.name}:attribute:action_set", party_id)


if __name__ == '__main__':
    party_io = PartyIO()

    # Adding a new party
    party_id = 123
    name = "New Party"
    date_formed = "2023-04-19"
    date_disbanded = ""
    party_type = "Team Thundar"
    entity_set = ""
    event_set = ""
    objective_set = ""
    action_set = ""

    party_io.add_party(party_id, name, date_formed, date_disbanded, party_type, entity_set, event_set, objective_set, action_set)

    # Deleting the party using its ID
    # party_io.delete_party(party_id)
