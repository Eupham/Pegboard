import subprocess
import uuid
import redis

class RedisManager:
    def __init__(self):
        self.redis_process = None
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


    def start_redis(self):
        if not self.redis_process:
            self.redis_process = subprocess.Popen(['redis-server', '--daemonize', 'yes'])
            print("Redis server started.")
        else:
            print("Redis server is already running.")

    def stop_redis(self):
        if self.redis_process:
            subprocess.run(['redis-cli', 'shutdown'])
            self.redis_process.wait()
            self.redis_process = None
            print("Redis server stopped.")
        else:
            print("Redis server is not running.")

    def add_task(self, date_time, assigned_entity, involved_entity, ass_ent_id, inv_ent_id, loc_id):
        task_id = str(uuid.uuid4())
        task_key = f"task:{task_id}"
        self.redis_client.hset(task_key, "ID", task_id)
        self.redis_client.hset(task_key, "DateTime", date_time)
        self.redis_client.hset(task_key, "AssignedEntity", assigned_entity)
        self.redis_client.hset(task_key, "InvolvedEntity", involved_entity)
        self.redis_client.hset(task_key, "AssEntID", ass_ent_id)
        self.redis_client.hset(task_key, "InvEntID", inv_ent_id)
        self.redis_client.hset(task_key, "LocID", loc_id)
        return task_id

    def add_entity(self, ent_typ_id, name, phone, email, site):
        ent_id = str(uuid.uuid4())
        entity_key = f"entity:{ent_id}"
        self.redis_client.hset(entity_key, "EntID", ent_id)
        self.redis_client.hset(entity_key, "EntTypID", ent_typ_id)
        self.redis_client.hset(entity_key, "Name", name)
        self.redis_client.hset(entity_key, "Phone", phone)
        self.redis_client.hset(entity_key, "Email", email)
        self.redis_client.hset(entity_key, "Site", site)
        return ent_id

    def add_entity_type(self, type_name):
        ent_typ_id = str(uuid.uuid4())
        entity_type_key = f"entity_type:{ent_typ_id}"
        self.redis_client.hset(entity_type_key, "EntTypID", ent_typ_id)
        self.redis_client.hset(entity_type_key, "TypeName", type_name)
        return ent_typ_id

    def add_location_type(self, type_name):
        loc_typ_id = str(uuid.uuid4())
        location_type_key = f"location_type:{loc_typ_id}"
        self.redis_client.hset(location_type_key, "LocTypID", loc_typ_id)
        self.redis_client.hset(location_type_key, "TypeName", type_name)
        return loc_typ_id

    def add_location(self, address, location_type, loc_typ_id):
        loc_id = str(uuid.uuid4())
        location_key = f"location:{loc_id}"
        self.redis_client.hset(location_key, "LocID", loc_id)
        self.redis_client.hset(location_key, "Address", address)
        self.redis_client.hset(location_key, "LocationType", location_type)
        self.redis_client.hset(location_key, "LocTypID", loc_typ_id)
        return loc_id
        
if __name__ == '__main__':
    redis_manager = RedisManager()

    # Add some sample data
    task_id = redis_manager.add_task("2022-01-01 10:00:00", "John Doe", "Jane Doe", "1", "2", "3")
    ent_typ_id = redis_manager.add_entity_type("Company")
    ent_id = redis_manager.add_entity(ent_typ_id, "ABC Inc.", "555-1234", "abc@inc.com", "www.abc.com")
    loc_typ_id = redis_manager.add_location_type("City")
    loc_id = redis_manager.add_location("123 Main St.", "New York City", loc_typ_id)

    # Print out the data we just added
    print("Tasks:")
    tasks = redis_manager.redis_client.keys("task:*")
    for task_key in tasks:
        task = redis_manager.redis_client.hgetall(task_key)
        print(task)
    print("Entities:")
    entities = redis_manager.redis_client.keys("entity:*")
    for entity_key in entities:
        entity = redis_manager.redis_client.hgetall(entity_key)
        print(entity)
    print("Location Types:")
    location_types = redis_manager.redis_client.keys("location_type:*")
    for location_type_key in location_types:
        location_type = redis_manager.redis_client.hgetall(location_type_key)
        print(location_type)
    print("Locations:")
    locations = redis_manager.redis_client.keys("location:*")
    for location_key in locations:
        location = redis_manager.redis_client.hgetall(location_key)
        print(location)
