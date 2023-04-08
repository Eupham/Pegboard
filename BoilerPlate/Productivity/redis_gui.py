import tkinter as tk
from tkinter import ttk
import redis


class RedisGUI:
    def __init__(self, root):
        self.root = root
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

        # Create tabs
        self.notebook = ttk.Notebook(self.root)
        self.task_frame = ttk.Frame(self.notebook)
        self.entity_frame = ttk.Frame(self.notebook)
        self.location_frame = ttk.Frame(self.notebook)
        self.loctyp_frame = ttk.Frame(self.notebook)
        self.enttyp_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.task_frame, text="Tasks")
        self.notebook.add(self.entity_frame, text="Entities")
        self.notebook.add(self.location_frame, text="Locations")
        self.notebook.add(self.loctyp_frame, text="Location Type")
        self.notebook.add(self.enttyp_frame, text="Entity Type")
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self.entity_data = self.get_entities()
        self.location_data = self.get_locations()
        self.entity_type_data = self.get_entity_types()
        self.location_type_data = self.get_location_types()

        # Create tables and entry forms
        self.create_table(self.task_frame, "task", combobox_columns=["AssEntID", "InvEntID", "LocID"])
        self.create_table(self.entity_frame, "entity", combobox_columns=["EntTypID"])
        self.create_table(self.location_frame, "location", combobox_columns=["LocTypID"])
        self.create_table(self.enttyp_frame, "entity_type")
        self.create_table(self.loctyp_frame, "location_type")

    def create_table(self, frame, hash_name, combobox_columns=None):
        if combobox_columns is None:
            combobox_columns = []

        table_data = {}
        table_keys = self.redis_client.keys(f"{hash_name}:*")
        for key in table_keys:
            decoded_key = key.decode()
            decoded_values = {k.decode(): v.decode() for k, v in self.redis_client.hgetall(key).items()}
            table_data[decoded_key] = decoded_values

        column_names = list(list(table_data.values())[0].keys())

        entry_form = ttk.Frame(frame)
        entry_widgets = {}

        for i, column in enumerate(column_names):
            label = ttk.Label(entry_form, text=column)
            label.grid(row=i, column=0)

            if column in combobox_columns:
                combobox_values = list(self.get_column_values(column).values())
                combobox = ttk.Combobox(entry_form, value=combobox_values, state="readonly")
                combobox.grid(row=i, column=1)

                # store the ID value in the entry_widgets dict for later use
                column_id = f"{column.lower()}"
                if column_id == "assentid" or column_id == "inventid":
                    column_id = "entid"
                else:
                    column_id = column_id
                entry_widgets[column_id] = {v: k.split(":")[-1] for k, v in self.get_column_values(column).items()}

                def combobox_selected(event, entry):
                    selected_value = combobox.get()
                    selected_id = entry_widgets[column_id].get(selected_value)
                    entry.delete(0, tk.END)
                    entry.insert(0, selected_id)
                    

                entry = ttk.Entry(entry_form)
                entry.grid(row=i, column=2)
                entry_widgets[column] = entry

                combobox.bind("<<ComboboxSelected>>", lambda event, e=entry: combobox_selected(event, e))
                
            else:
                entry = ttk.Entry(entry_form)
                entry.grid(row=i, column=1)
                entry_widgets[column] = entry

        add_button = ttk.Button(entry_form, text="Add", command=lambda: self.add_record(hash_name, entry_widgets, table_treeview))
        add_button.grid(row=len(column_names), column=0)

        update_button = ttk.Button(entry_form, text="Update", command=lambda: self.update_record(hash_name, entry_widgets, table_treeview))
        update_button.grid(row=len(column_names), column=1)

        delete_button = ttk.Button(entry_form, text="Delete", command=lambda: self.delete_record(hash_name, table_treeview))
        delete_button.grid(row=len(column_names), column=2)

        entry_form.pack(side="top", fill="x")

        table_treeview = ttk.Treeview(frame, columns=column_names, show="headings")
        for column in column_names:
            table_treeview.heading(column, text=column)

        for key, values in table_data.items():
            table_treeview.insert("", "end", value=list(values.values()))

        table_treeview.pack(side="left", fill="both")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table_treeview.yview)
        scrollbar.pack(side="right", fill="y")
        table_treeview.configure(yscrollcommand=scrollbar.set)

        table_treeview.bind('<ButtonRelease-1>', lambda event: self.tree_row_click(event, table_treeview, entry_widgets))

    def get_column_values(self, column_name):
        if column_name == "AssEntID" or column_name == "InvEntID":
            data = self.entity_data
            prefix = "entity:"
            field = "Name"
        elif column_name == "LocID":
            data = self.location_data
            prefix = "location:"
            field = "Address"
        elif column_name == "EntTypID":
            data = self.entity_type_data
            prefix = "entity_type:"
            field = "TypeName"
        elif column_name == "LocTypID":
            data = self.entity_type_data
            prefix = "location_type:"
            field = "TypeName"

        else:
            return {}

        return {k.replace(prefix, ""): v[field] for k, v in data.items() if field in v}

    def get_entities(self):
        entity_keys = self.redis_client.keys("entity:*")
        entities = {}
        for key in entity_keys:
            decoded_key = key.decode()
            decoded_values = {k.decode(): v.decode() for k, v in self.redis_client.hgetall(key).items()}
            entities[decoded_key] = decoded_values
        return entities

    def get_entity_types(self):
        entity_type_keys = self.redis_client.keys("entity_type:*")
        entity_types = {}
        for key in entity_type_keys:
            decoded_key = key.decode()
            decoded_values = {k.decode(): v.decode() for k, v in self.redis_client.hgetall(key).items()}
            entity_types[decoded_key] = decoded_values
        return entity_types

    def get_locations(self):
        location_keys = self.redis_client.keys("location:*")
        locations = {}
        for key in location_keys:
            decoded_key = key.decode()
            decoded_values = {k.decode(): v.decode() for k, v in self.redis_client.hgetall(key).items()}
            locations[decoded_key] = decoded_values
        return locations

    def get_location_types(self):
        location_type_keys = self.redis_client.keys("location_type:*")
        location_types = {}
        for key in location_type_keys:
            decoded_key = key.decode()
            decoded_values = {k.decode(): v.decode() for k, v in self.redis_client.hgetall(key).items()}
            location_types[decoded_key] = decoded_values
        return location_types

    def tree_row_click(self, event, treeview, entry_widgets):
        item = treeview.selection()[0]
        row_values = treeview.item(item, 'values')

        for i, value in enumerate(row_values):
            column = treeview.column(i, option='id')
            entry_widgets[column].delete(0, tk.END)
            entry_widgets[column].insert(0, value)

    def add_record(self, hash_name, entry_widgets, table_treeview):
        new_values = {column: entry.get() for column, entry in entry_widgets.items()}
        new_key = f"{hash_name}:{max([int(k.split(':')[1]) for k in self.redis_client.keys(f'{hash_name}:*')]) + 1}"

        self.redis_client.hmset(new_key, new_values)
        table_treeview.insert("", "end", value=list(new_values.values()))

    def update_record(self, hash_name, entry_widgets, table_treeview):
        item = table_treeview.selection()[0]
        row_key = table_treeview.item(item, 'text')
        updated_values = {column: entry.get() for column, entry in entry_widgets.items()}

        self.redis_client.hmset(row_key, updated_values)
        table_treeview.item(item, value=list(updated_values.values()))

    def delete_record(self, hash_name, table_treeview):
        item = table_treeview.selection()[0]
        row_key = table_treeview.item(item, 'text')

        self.redis_client.delete(row_key)
        table_treeview.delete(item)

if __name__ == "__main__":
    root = tk.Tk()
    app = RedisGUI(root)
    root.mainloop()