import redis

client = redis.Redis(host='localhost', port=6379, db=0)

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

def create_all_module_objects():
    for module_name, module_data in MODULES.items():
        create_module_properties(module_name, module_data["properties"])
        create_module_attributes(module_name, module_data["attributes"])
        create_module_metadata(module_name, module_data["metadata"])

def create_module_properties(module_name, property):
    for property in property:
        client.zadd(f"{module_name}:property:{property}", {"": 0})

def create_module_attributes(module_name, attributes):
    for attribute in attributes:
        client.zadd(f"{module_name}:attribute:{attribute}", {"": 0})

def create_module_metadata(module_name, metadata):
    for metadata_item in metadata:
        client.zadd(f"{module_name}:metadata:{metadata_item}", {"": 0})

class entity_CRUD:
    def __init__(self, client):
        self.client = client
    
    def create(self, entity_id, name, date_initiated, date_inactive, entity_type, objective_set=None, party_set=None, party_role_set=None, description=None, contact_hashes=None):
        entity_key = f"entity:{entity_id}"
        entity_data = {
            "name": name,
            "date_initiated": date_initiated,
            "date_inactive": date_inactive,
            "type": entity_type
        }
        if objective_set:
            entity_data["objective_set"] = objective_set
        if party_set:
            entity_data["party_set"] = party_set
        if party_role_set:
            entity_data["party_role_set"] = party_role_set
        if description:
            entity_data["description"] = description
        if contact_hashes:
            entity_data["contact_hashes"] = contact_hashes
        
        self.client.hmset(entity_key, entity_data)
    
    def read(self, entity_id):
        entity_key = f"entity:{entity_id}"
        entity_data = self.client.hgetall(entity_key)
        return entity_data
    
    def update(self, entity_id, updated_data):
        entity_key = f"entity:{entity_id}"
        self.client.hmset(entity_key, updated_data)
    
    def delete(self, entity_id):
        entity_key = f"entity:{entity_id}"
        self.client.delete(entity_key)

class party_CRUD:
    def __init__(self, name, date_formed, date_disbanded, entity_set=None, event_set=None, objective_set=None, action_set=None):
        self.id = client.incr("party:id")
        self.name = name
        self.date_formed = date_formed
        self.date_disbanded = date_disbanded
        self.entity_set = entity_set or set()
        self.event_set = event_set or set()
        self.objective_set = objective_set or set()
        self.action_set = action_set or set()

    def save(self):
        pipe = client.pipeline()
        key = f"party:{self.id}"
        data = {
            "id": self.id,
            "name": self.name,
            "date_formed": self.date_formed,
            "date_disbanded": self.date_disbanded,
            "entity_set": list(self.entity_set),
            "event_set": list(self.event_set),
            "objective_set": list(self.objective_set),
            "action_set": list(self.action_set)
        }
        pipe.hmset(key, data)
        pipe.execute()

    def load(self, id):
        key = f"party:{id}"
        data = client.hgetall(key)
        if not data:
            return None
        entity_set = set(data.get("entity_set", []))
        event_set = set(data.get("event_set", []))
        objective_set = set(data.get("objective_set", []))
        action_set = set(data.get("action_set", []))
        return Party(data["name"], data["date_formed"], data["date_disbanded"], entity_set, event_set, objective_set, action_set)

    def add_entity(self, entity):
        self.entity_set.add(entity.id)
        self.save()

    def remove_entity(self, entity):
        self.entity_set.discard(entity.id)
        self.save()

    def add_event(self, event):
        self.event_set.add(event.id)
        self.save()

    def remove_event(self, event):
        self.event_set.discard(event.id)
        self.save()

    def add_objective(self, objective):
        self.objective_set.add(objective.id)
        self.save()

    def remove_objective(self, objective):
        self.objective_set.discard(objective.id)
        self.save()

    def add_action(self, action):
        self.action_set.add(action.id)
        self.save()

    def remove_action(self, action):
        self.action_set.discard(action.id)
        self.save()


class event_CRUD:
    def __init__(self, name, location, datetime_start, datetime_end, party_set=None, result_set=None):
        self.id = client.incr("event:id")
        self.name = name
        self.location = location
        self.datetime_start = datetime_start
        self.datetime_end = datetime_end
        self.party_set = party_set or set()
        self.result_set = result_set or set()

    def save(self):
        pipe = client.pipeline()
        key = f"event:{self.id}"
        data = {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "datetime_start": self.datetime_start,
            "datetime_end": self.datetime_end,
            "party_set": list(self.party_set),
            "result_set": list(self.result_set),
        }
        pipe.hmset(key, data)
        pipe.execute()

    def load(self, id):
        key = f"event:{id}"
        data = client.hgetall(key)
        if not data:
            return None
        party_set = set(data.get("party_set", []))
        result_set = set(data.get("result_set", []))
        return Event(data["name"], data["location"], data["datetime_start"], data["datetime_end"], party_set, result_set)

    def add_party(self, party):
        self.party_set.add(party.id)
        self.save()

    def remove_party(self, party):
        self.party_set.discard(party.id)
        self.save()

    def add_result(self, result):
        self.result_set.add(result.id)
        self.save()

    def remove_result(self, result):
        self.result_set.discard(result.id)
        self.save()

class nash_CRUD:
    def __init__(self, datastore):
        self.datastore = datastore
    
    def create(self, name, event_set=None, interest_weight_set=None, payoff_set=None):
        nash_id = str(uuid.uuid4())
        nash = {
            "id": nash_id,
            "name": name,
            "event_set": event_set or [],
            "interest_weight_set": interest_weight_set or [],
            "payoff_set": payoff_set or []
        }
        self.datastore["nash"][nash_id] = nash
        return nash
    
    def read(self, nash_id):
        return self.datastore["nash"].get(nash_id)
    
    def update(self, nash_id, name=None, event_set=None, interest_weight_set=None, payoff_set=None):
        nash = self.datastore["nash"].get(nash_id)
        if not nash:
            return None
        if name:
            nash["name"] = name
        if event_set:
            nash["event_set"] = event_set
        if interest_weight_set:
            nash["interest_weight_set"] = interest_weight_set
        if payoff_set:
            nash["payoff_set"] = payoff_set
        return nash
    
    def delete(self, nash_id):
        nash = self.datastore["nash"].get(nash_id)
        if not nash:
            return False
        del self.datastore["nash"][nash_id]
        return True
    
    def list(self):
        return list(self.datastore["nash"].values())
    
    def add_event(self, nash_id, event_id):
        nash = self.datastore["nash"].get(nash_id)
        event = self.datastore["event"].get(event_id)
        if not nash or not event:
            return False
        if event_id not in nash["event_set"]:
            nash["event_set"].append(event_id)
        return True
    
    def remove_event(self, nash_id, event_id):
        nash = self.datastore["nash"].get(nash_id)
        if not nash:
            return False
        try:
            nash["event_set"].remove(event_id)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    create_all_module_objects()

    party = party_CRUD("Party A", "2023-04-19", "2023-04-20")
    party.save()

    entity1 = entity_CRUD(client)
    entity1.create("entity1", "Entity 1", "2023-04-19", "2023-04-20", "Type A")
    entity2 = entity_CRUD(client)
    entity2.create("entity2", "Entity 2", "2023-04-19", "2023-04-20", "Type B")
    entity3 = entity_CRUD(client)
    entity3.create("entity3", "Entity 3", "2023-04-19", "2023-04-20", "Type C")

    party.add_entity(entity1)
    party.add_entity(entity2)
    party.add_entity(entity3)

    event = event_CRUD("Event X", "Location A", "2023-04-19 08:00:00", "2023-04-19 12:00:00")
    event.save()

    event.add_party(party)

    nash_scenario = nash_CRUD("Nash Scenario 1", "2023-04-19", "2023-04-20")
    nash_scenario.save()

    nash_scenario.add_event(event)