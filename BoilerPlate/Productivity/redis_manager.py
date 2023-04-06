import subprocess
import uuid
import redis

class RedisManager:
    def __init__(self):
        self.redis_process = None
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


    def start_redis(self):
        if not self.redis_process:
            self.redis_process = subprocess.Popen(['redis-server', 'daemonize', 'yes'])
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
        self.redis_client.hmset(task_key, {
            "ID": task_id,
            "DateTime": date_time,
            "AssignedEntity": assigned_entity,
            "InvolvedEntity": involved_entity,
            "AssEntID": ass_ent_id,
            "InvEntID": inv_ent_id,
            "LocID": loc_id
        })
        return task_id

    def add_entity(self, ent_typ_id, name, phone, email, site):
        ent_id = str(uuid.uuid4())
        entity_key = f"entity:{ent_id}"
        self.redis_client.hmset(entity_key, {
            "EntID": ent_id,
            "EntTypID": ent_typ_id,
            "Name": name,
            "Phone": phone,
            "Email": email,
            "Site": site
        })
        return ent_id

    def add_entity_type(self, type_name):
        ent_typ_id = str(uuid.uuid4())
        entity_type_key = f"entity_type:{ent_typ_id}"
        self.redis_client.hmset(entity_type_key, {
            "EntTypID": ent_typ_id,
            "TypeName": type_name
        })
        return ent_typ_id

    def add_location_type(self, type_name):
        loc_typ_id = str(uuid.uuid4())
        location_type_key = f"location_type:{loc_typ_id}"
        self.redis_client.hmset(location_type_key, {
            "LocTypID": loc_typ_id,
            "TypeName": type_name
        })
        return loc_typ_id

    def add_location(self, address, location_type, loc_typ_id):
        loc_id = str(uuid.uuid4())
        location_key = f"location:{loc_id}"
        self.redis_client.hmset(location_key, {
            "LocID": loc_id,
            "Address": address,
            "LocationType": location_type,
            "LocTypId": loc_typ_id
        })
        return loc_id
