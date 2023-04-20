#PlurInit.py

import redis

client = redis.Redis(host='localhost', port=6379, db=0)

class Plurals:
    def __init__(self, name, parties, entities, events, actions, results, objectives, roles):
        self.name = name
        self.parties = parties
        self.entities = entities
        self.events = events
        self.actions = actions
        self.results = results
        self.roles = roles
        self.objectives = objectives
        self.client = redis.Redis(host='localhost', port=6379, db=0)
        self.create_sets([
            ("parties", self.parties),
            ("entities", self.entities),
            ("events", self.events),
            ("actions", self.actions),
            ("results", self.results),
            ("objectives", self.objectives),
            ("roles", self.roles)
        ])

    def create_sets(self, category_data):
        for category, data_list in category_data:
            for data in data_list:
                self.client.zadd(f"{self.name}:{category}:{data}", {"": 0})

class PluralInit:
    PLURALS = {
        "sets": {
            "parties": ["set_id", "id"],
            "entities": ["set_id", "id"],
            "events": ["set_id", "id"],
            "actions": ["set_id", "id"],
            "results": ["set_id", "id"],
            "objectives": ["set_id", "id"],
            "roles": ["set_id", "id"]
        }
    }

    def __init__(self):
        self.plurals = []
        for plural_name, plural_data in self.PLURALS.items():
            plural = Plurals(plural_name, plural_data["parties"], plural_data["entities"], plural_data["events"], plural_data["actions"], plural_data["results"], plural_data["objectives"], plural_data["roles"])
            self.plurals.append(plural)

    def create_plurals(self):
        for plural in self.plurals:
            plural.create_sets([
                ("parties", plural.parties),
                ("entities", plural.entities),
                ("events", plural.events),
                ("actions", plural.actions),
                ("results", plural.results),
                ("objectives", plural.objectives),
                ("roles", plural.roles)
            ])

if __name__ == '__main__':
    plurinit = PluralInit()
    plurinit.create_plurals()