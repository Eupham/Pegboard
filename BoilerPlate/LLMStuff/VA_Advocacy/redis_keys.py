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
    for property in properties:
        client.zadd(f"{module_name}:property:{property}", {"": 0})

def create_module_attributes(module_name, attributes):
    for attribute in attributes:
        client.zadd(f"{module_name}:attribute:{attribute}", {"": 0})

def create_module_metadata(module_name, metadata):
    for metadata_item in metadata:
        client.zadd(f"{module_name}:metadata:{metadata_item}", {"": 0})

create_all_module_objects()