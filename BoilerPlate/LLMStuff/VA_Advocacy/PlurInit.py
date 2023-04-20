#PlurInit.py

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
        for party in self.parties:
            self.client.zadd(f"{self.name}:parties:{party}", {"": 0})

    def create_entities_set(self):
        for entity in self.entities:
            self.client.zadd(f"{self.name}:entities:{entity}", {"": 0})

    def create_events_set(self):
        for event in self.events:
            self.client.zadd(f"{self.name}:events:{event}", {"": 0})
    

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
            plural = Plurals(plural_name, plural_data["parties"], plural_data["entities"], plural_data["events"])
            self.plurals.append(plural)

    def create_plurals(self):
        for plural in self.plurals:
            plural.create_parties_set()
            plural.create_entities_set()
            plural.create_events_set()

if __name__ == '__main__':
    plurinit = PluralInit()
    plurinit.create_plurals()