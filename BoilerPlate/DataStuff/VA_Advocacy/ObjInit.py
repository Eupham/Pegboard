#ObjInit.py

import redis

client = redis.Redis(host='localhost', port=6379, db=0)

class ObjectiveInit:
    MODULES = {
        "objectives": {
            "properties": ["name"],
            "attributes": ["type", "Action_Set", "Result_Set"],
            "metadata": ["id", "description"]
        },
        "actions": {
            "properties": ["name", "Result_Set"],
            "attributes": ["type", "Monetary_Cost_Fcst", "Time_Cost_Fcst", "Entity_Cost_Fcst"],
            "metadata": ["id", "description"]
        },
        "results": {
            "properties": ["name"],
            "attributes": ["type", "Monetary_Cost_Actl", "Time_Cost_Actl", "Entity_Cost_Actl"],
            "metadata": ["id", "description"]
        }
    }

    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0)

    def create_module_set(self, module_name, set_type, values):
        for value in values:
            self.client.zadd(f"{module_name}:{set_type}:{value}", {"": 0})

    def create_modules(self):
        for module_name, module_data in self.MODULES.items():
            for set_type in ["properties", "attributes", "metadata"]:
                self.create_module_set(module_name, set_type, module_data[set_type])

if __name__ == '__main__':
    objinit = ObjectiveInit()
    objinit.create_modules()