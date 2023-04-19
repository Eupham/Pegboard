import redis

client = redis.Redis(host='localhost', port=6379, db=0)

MODULES = {
    "party": {
        "attributes": ["name", "location", "date"],
        "metadata": ["id", "description"]
    },
    "entity": {
        "attributes": ["name", "interests", "contact_hashes"],
        "metadata": ["id", "results"]
    },
    "event": {
        "attributes": ["name", "location", "date"],
        "metadata": ["id", "description"]
    },
    "nash": {
        "attributes": ["name", "location", "date"],
        "metadata": ["id", "description"]
    },
    "integration": {
        "attributes": ["name", "location", "date"],
        "metadata": ["id", "description"]
    }
}

def create_all_module_objects():
    for module_name, module_data in MODULES.items():
        create_module_attributes(module_name, module_data["attributes"])
        create_module_metadata(module_name, module_data["metadata"])

def create_module_attributes(module_name, attributes):
    for attribute in attributes:
        client.zadd(f"{module_name}:attribute:{attribute}", {"": 0})

def create_module_metadata(module_name, metadata):
    for metadata_item in metadata:
        client.zadd(f"{module_name}:metadata:{metadata_item}", {"": 0})

create_all_module_objects()
