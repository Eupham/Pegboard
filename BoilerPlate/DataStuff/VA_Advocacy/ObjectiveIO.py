#ObjectiveIO.py

import redis
from ObjInit import ObjectiveInit

modinit = ObjectiveInit()

class ObjectiveIO:
    def init(self):
        self.obj_module = modinit.modules[0]

    def add_objective(self, objective_id, name, action, outcome, objective_type, monetary_cost, time_cost, entity_cost):
        self.obj_module.client.zadd(f"{self.obj_module.name}:metadata:id", {objective_id: 0})
        self.obj_module.client.zadd(f"{self.obj_module.name}:property:name", {name: objective_id})
        self.obj_module.client.zadd(f"{self.obj_module.name}:property:Action", {action: objective_id})
        self.obj_module.client.zadd(f"{self.obj_module.name}:property:Outcome", {outcome: objective_id})
        self.obj_module.client.zadd(f"{self.obj_module.name}:attribute:type", {objective_type: objective_id})
        self.obj_module.client.zadd(f"{self.obj_module.name}:attribute:Monetary_Cost", {monetary_cost: objective_id})
        self.obj_module.client.zadd(f"{self.obj_module.name}:attribute:Time_Cost", {time_cost: objective_id})
        self.obj_module.client.zadd(f"{self.obj_module.name}:attribute:Entity_Cost", {entity_cost: objective_id})

    def delete_objective(self, objective_id):
        self.obj_module.client.zrem(f"{self.obj_module.name}:metadata:id", objective_id)
        self.obj_module.client.zrem(f"{self.obj_module.name}:property:name", objective_id)
        self.obj_module.client.zrem(f"{self.obj_module.name}:property:Action_Set", objective_id)
        self.obj_module.client.zrem(f"{self.obj_module.name}:property:Outcome_Set", objective_id)
        self.obj_module.client.zrem(f"{self.obj_module.name}:attribute:type", objective_id)
        self.obj_module.client.zrem(f"{self.obj_module.name}:attribute:Monetary_Cost", objective_id)
        self.obj_module.client.zrem(f"{self.obj_module.name}:attribute:Time_Cost", objective_id)
        self.obj_module.client.zrem(f"{self.obj_module.name}:attribute:Entity_Cost", objective_id)

if __name__ == '__main__':
    objective_io = ObjectiveIO()
    objective_io.add_objective(
        objective_id=456,
        name="New Objective",
        action="Do Something",
        outcome="Achieve Something",
        objective_type="Type A",
        monetary_cost="5000 USD",
        time_cost="1 week",
        entity_cost="5 entities"
    )

    # Deleting an objective by id
    objective_id_to_delete = 456
    objective_io.delete_objective(objective_id_to_delete)