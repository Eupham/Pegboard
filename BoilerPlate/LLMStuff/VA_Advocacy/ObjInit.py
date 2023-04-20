#ObjInit.py

import redis

client = redis.Redis(host='localhost', port=6379, db=0)

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
        "objectives": {
            "properties": ["name", "Action", "Outcome"],
            "attributes": ["type", "Monetary_Cost", "Time_Cost", "Entity_Cost"],
            "metadata": ["id", "description"]
        }
    }
#Objective	Action	Outcome
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
    objinit = ModuleInit()
    objinit.create_modules()