#NashIO.py

import redis
from ModInit import ModuleInit

modinit = ModuleInit()

class NashIO:
    def __init__(self):
        self.nash_module = modinit.modules[3]

    def add_nash(self, nash_id, name, event_set, interest_weight_set, payoff_set):
        self.nash_module.client.zadd(f"{self.nash_module.name}:metadata:id", {nash_id: 0})
        self.nash_module.client.zadd(f"{self.nash_module.name}:property:name", {name: nash_id})
        self.nash_module.client.zadd(f"{self.nash_module.name}:attribute:event_set", {event_set: nash_id})
        self.nash_module.client.zadd(f"{self.nash_module.name}:attribute:interest_weight_set", {interest_weight_set: nash_id})
        self.nash_module.client.zadd(f"{self.nash_module.name}:attribute:payoff_set", {payoff_set: nash_id})

    def delete_nash(self, nash_id):
        self.nash_module.client.zrem(f"{self.nash_module.name}:metadata:id", nash_id)
        self.nash_module.client.zremrangebyscore(f"{self.nash_module.name}:property:name", nash_id, nash_id)
        self.nash_module.client.zremrangebyscore(f"{self.nash_module.name}:attribute:event_set", nash_id, nash_id)
        self.nash_module.client.zremrangebyscore(f"{self.nash_module.name}:attribute:interest_weight_set", nash_id, nash_id)
        self.nash_module.client.zremrangebyscore(f"{self.nash_module.name}:attribute:payoff_set", nash_id, nash_id)

if __name__ == '__main__':
    nash_io = NashIO()

    # Adding a new Nash equilibrium to the "nash" module
    nash_id = 456
    nash_name = "New Nash"
    nash_event_set = "789"
    nash_interest_weight_set = "123"
    nash_payoff_set = "456"

    nash_io.add_nash(nash_id, nash_name, nash_event_set, nash_interest_weight_set, nash_payoff_set)

    # Deleting the Nash equilibrium using its ID
    nash_io.delete_nash(nash_id)
