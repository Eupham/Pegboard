import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from tkcalendar import DateEntry
from tktimepicker import AnalogPicker
from datetime import datetime
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
        self.create_table(self.task_frame, "task")
        self.create_table(self.entity_frame, "entity")
        self.create_table(self.location_frame, "location")
        self.create_table(self.enttyp_frame, "entity_type")
        self.create_table(self.loctyp_frame, "location_type")

    def create_table(self, frame, hash_name):
        table_data = {}
        table_keys = self.redis_client.keys(f"{hash_name}:*")
        for key in table_keys:
            decoded_key = key.decode()
            decoded_values = {k.decode(): v.decode() for k, v in self.redis_client.hgetall(key).items()}
            table_data[decoded_key] = decoded_values

        column_names = list(list(table_data.values())[0].keys())

        entry_widgets = self.create_entry_form(frame, column_names, hash_name)
        table_treeview = self.create_table_treeview(frame, column_names, table_data, entry_widgets)

    def show_time_picker(self, time_button):
        picker_window = Toplevel()
        picker_frame = ttk.Frame(picker_window)

        picker = AnalogPicker(picker_frame)

        def on_time_select():
            time_str = datetime.strptime(picker.selected_time, "%H:%M").strftime("%I:%M %p")
            entry_widget.config(state="normal")
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, time_str)
            entry_widget.config(state="readonly")
            picker_window.destroy()

        confirm_button = ttk.Button(picker_frame, text="Confirm", command=on_time_select)

        picker.pack(side="left", fill="both")
        confirm_button.pack(side="right", padx=5)

        picker_frame.pack(fill="both", expand=True)


    def create_entry_form(self, frame, column_names, hash_name):
        entry_form = ttk.Frame(frame)
        entry_widgets = {}
        related_treeview_frame = ttk.Frame(frame)  # Add a new frame for the related Treeview

        for i, column in enumerate(column_names):
            label = ttk.Label(entry_form, text=column)
            label.grid(row=i, column=0)

            if column == "DateTime":
                date_entry = DateEntry(entry_form, format='%m/%d/%Y')
                date_entry.grid(row=i, column=1)
                entry_widgets["Date"] = date_entry

                time_label = ttk.Label(entry_form, text="00:00:00")
                time_label.grid(row=i, column=2)
                entry_widgets["Time"] = time_label

                # Bind the label's double click event to show_time_picker method
                time_label.bind('<Double-Button-1>', lambda event: self.show_time_picker(entry_widgets["Time"]))

            else:
                entry = ttk.Entry(entry_form)
                entry.grid(row=i, column=1)
                entry_widgets[column] = entry

                # Bind the Entry's click event to show_related_treeview method
                if column in ["AssEntID", "InvEntID", "LocID", "EntTypID", "LocTypID"]:
                    entry.bind('<Button-1>', lambda event, col=column, frame=related_treeview_frame, entry=entry_widgets[column]: self.show_related_treeview(col, frame, entry))

        add_button = ttk.Button(entry_form, text="Add", command=lambda: self.add_record(hash_name, entry_widgets, table_treeview))
        add_button.grid(row=len(column_names), column=0)

        update_button = ttk.Button(entry_form, text="Update", command=lambda: self.update_record(hash_name, entry_widgets, table_treeview))
        update_button.grid(row=len(column_names), column=1)

        delete_button = ttk.Button(entry_form, text="Delete", command=lambda: self.delete_record(hash_name, table_treeview))
        delete_button.grid(row=len(column_names), column=2)

        entry_form.pack(side="left", fill="y")  # Update the packing to 'left'
        related_treeview_frame.pack(side="left", fill="both")  # Pack the new frame to the right of the entry_form

        entry_form.pack(side="top", fill="x")
        return entry_widgets


    def create_table_treeview(self, frame, column_names, table_data, entry_widgets):
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
        return table_treeview

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
            if column == "DateTime":
                date_value, time_value = value.split(" ")
                entry_widgets["Date"].delete(0, tk.END)
                entry_widgets["Date"].insert(0, date_value)
                entry_widgets["Time"].config(text=time_value) # Update the time label
            else:
                entry_widgets[column].delete(0, tk.END)
                entry_widgets[column].insert(0, value)

    def get_column_values(self, column_name):
        column_info = {
            "AssEntID": {"data": self.entity_data, "prefix": "entity:", "field": "Name"},
            "InvEntID": {"data": self.entity_data, "prefix": "entity:", "field": "Name"},
            "LocID": {"data": self.location_data, "prefix": "location:", "field": "Address"},
            "EntTypID": {"data": self.entity_type_data, "prefix": "entity_type:", "field": "TypeName"},
            "LocTypID": {"data": self.location_type_data, "prefix": "location_type:", "field": "TypeName"},
        }

        for key, info in column_info.items():
            if column_name == key:
                data = info["data"]
                prefix = info["prefix"]
                field = info["field"]
                return {k.replace(prefix, ""): v[field] for k, v in data.items() if field in v}

        return {}

    def show_related_treeview(self, column_name, related_treeview_frame, entry_widget):
        related_data = self.get_column_values(column_name)

        # Destroy any existing Treeview in the frame
        for child in related_treeview_frame.winfo_children():
            child.destroy()

        related_treeview = ttk.Treeview(related_treeview_frame, columns=["ID", "Name"], show="headings")
        related_treeview.heading("ID", text="ID")
        related_treeview.heading("Name", text="Name")

        for key, value in related_data.items():
            related_treeview.insert("", "end", value=[key, value])

        related_treeview.pack(side="left", fill="both")
        scrollbar = ttk.Scrollbar(related_treeview_frame, orient="vertical", command=related_treeview.yview)
        scrollbar.pack(side="right", fill="y")
        related_treeview.configure(yscrollcommand=scrollbar.set)

        related_treeview.bind('<ButtonRelease-1>', lambda event, entry=entry_widget: self.related_treeview_row_click(event, related_treeview, entry))

    def related_treeview_row_click(self, event, related_treeview, entry_widget):
        item = related_treeview.selection()[0]
        row_values = related_treeview.item(item, 'values')
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, row_values[0])


    def add_record(self, hash_name, entry_widgets, table_treeview):
        new_values = {column: entry.get() for column, entry in entry_widgets.items() if column not in ["Date", "Time"]}
        new_values["DateTime"] = f"{entry_widgets['Date'].get()} {entry_widgets['Time'].get()}"

        new_key = f"{hash_name}:{max([int(k.split(':')[1]) for k in self.redis_client.keys(f'{hash_name}:*')]) + 1}"
        self.redis_client.hmset(new_key, new_values)

        # Adjust the values list to include the combined DateTime field
        display_values = list(new_values.values())
        display_values.insert(display_values.index(new_values["DateTime"]), new_values["DateTime"])
        display_values.remove(new_values["Date"])
        display_values.remove(new_values["Time"])

        table_treeview.insert("", "end", value=display_values)


    def update_record(self, hash_name, entry_widgets, table_treeview):
        item = table_treeview.selection()[0]
        row_key = table_treeview.item(item, 'text')
        updated_values = {column: entry.get() for column, entry in entry_widgets.items() if column not in ["Date", "Time"]}
        updated_values["DateTime"] = f"{entry_widgets['Date'].get()} {entry_widgets['Time'].get()}"

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