#sap_schemas_template.py
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

data_structures_dict = {
    "PP": ["Material_Master", "Bill_of_Materials", "Work_Center", "Routing", "Production_Order"],
    "MM": ["Material_Master", "Vendor_Master", "Purchase_Order", "Goods_Receipt", "Inventory_Management", "Invoice_Verification"],
    "QM": ["Inspection_Lot", "Inspection_Plan", "Quality_Notification", "Quality_Certificate"],
    "SD": ["Customer_Master", "Sales_Order", "Delivery", "Billing_Document"],
    "PM": ["Equipment_Master", "Functional_Location", "Maintenance_Order", "Maintenance_Notification"],
    "PS": ["Project_Definition", "Work_Breakdown_Structure", "Network", "Activity", "Cost_Planning"]
}

# Use Redis sets to store data structures under each module
for module, data_structures in data_structures_dict.items():
    for data_structure in data_structures:
        redis_client.sadd(f"Module:{module}", data_structure)

# Retrieve the data structures for each module from the sets and print them
for module in data_structures_dict.keys():
    owned_data_structures = redis_client.smembers(f"Modules:{module}")
    owned_data_structures_str = ', '.join([x.decode('utf-8') for x in owned_data_structures])
    print(f"{module}: {owned_data_structures_str}")

data_structures = {
    "Material_Master": {
        "material_id": "int",
        "material_name": "str",
        "material_type": "str",
        "unit_of_measure": "str",
        "plant": "str",
        "storage_location": "str"
    },
    "Bill_of_Materials": {
        "bom_id": "int",
        "material_id": "int",
        "component_id": "int",
        "component_quantity": "float",
        "unit_of_measure": "str",
        "valid_from": "str",
        "valid_to": "str"
    },
    "Work_Center": {
        "work_center_id": "int",
        "work_center_name": "str",
        "plant": "str",
        "cost_center": "str",
        "activity_type": "str",
        "capacity": "float"
    },
    "Routing": {
        "routing_id": "int",
        "material_id": "int",
        "plant": "str",
        "operation_id": "int",
        "work_center_id": "int",
        "control_key": "str",
        "duration": "float",
        "unit_of_duration": "str"
    },
    "Production_Order": {
        "production_order_id": "int",
        "material_id": "int",
        "plant": "str",
        "order_type": "str",
        "order_status": "str",
        "planned_start_date": "str",
        "planned_end_date": "str",
        "actual_start_date": "str",
        "actual_end_date": "str"
    },
    "Vendor_Master": {
        "vendor_id": "int",
        "vendor_name": "str",
        "address": "str",
        "city": "str",
        "postal_code": "str",
        "country": "str",
        "payment_terms": "str",
        "currency": "str"
    },
    "Purchase_Order": {
        "purchase_order_id": "int",
        "vendor_id": "int",
        "material_id": "int",
        "order_quantity": "float",
        "unit_of_measure": "str",
        "delivery_date": "str",
        "plant": "str",
        "storage_location": "str"
    },
    "Goods_Receipt": {
        "goods_receipt_id": "int",
        "purchase_order_id": "int",
        "material_id": "int",
        "quantity_received": "float",
        "unit_of_measure": "str",
        "movement_type": "str",
        "posting_date": "str",
        "plant": "str",
        "storage_location": "str"
    },
    "Inventory_Management": {
        "inventory_id": "int",
        "material_id": "int",
        "plant": "str",
        "storage_location": "str",
        "stock_type": "str",
        "quantity": "float",
        "unit_of_measure": "str"
    },
    "Invoice_Verification": {
        "invoice_id": "int",
        "vendor_id": "int",
        "purchase_order_id": "int",
        "invoice_date": "str",
        "invoice_amount": "float",
        "payment_status": "str",
        "currency": "str"
    },
    "Inspection_Lot": {
        "inspection_lot_id": "int",
        "material_id": "int",
        "plant": "str",
        "inspection_type": "str",
        "inspection_status": "str",
        "created_date": "str",
        "inspection_start_date": "str",
        "inspection_end_date": "str"
    },
    "Inspection_Plan": {
        "inspection_plan_id": "int",
        "material_id": "int",
        "plant": "str",
        "valid_from": "str",
        "valid_to": "str",
        "status": "str",
        "created_date": "str",
        "last_updated": "str"
    },
    "Quality_Notification": {
        "notification_id": "int",
        "material_id": "int",
        "plant": "str",
        "notification_type": "str",
        "created_date": "str",
        "status": "str",
        "description": "str",
        "priority": "str"
    },
    "Quality_Certificate": {
        "certificate_id": "int",
        "material_id": "int",
        "vendor_id": "int",
        "issue_date": "str",
        "expiration_date": "str",
        "certificate_status": "str"
    },
    "Customer_Master": {
        "customer_id": "int",
        "customer_name": "str",
        "address": "str",
        "city": "str",
        "postal_code": "str",
        "country": "str",
        "payment_terms": "str",
        "currency": "str"
    },
    "Sales_Order": {
        "sales_order_id": "int",
        "customer_id": "int",
        "material_id": "int",
        "order_quantity": "float",
        "unit_of_measure": "str",
        "requested_delivery_date": "str",
        "net_price": "float",
        "currency": "str",
        "order_status": "str"
    },
    "Delivery": {
        "delivery_id": "int",
        "sales_order_id": "int",
        "material_id": "int",
        "delivered_quantity": "float",
        "unit_of_measure": "str",
        "delivery_date": "str",
        "shipping_status": "str"
    },
    "Billing_Document": {
        "billing_document_id": "int",
        "sales_order_id": "int",
        "customer_id": "int",
        "billing_date": "str",
        "total_amount": "float",
        "currency": "str",
        "payment_status": "str"
    },
    "Equipment_Master": {
        "equipment_id": "int",
        "equipment_name": "str",
        "equipment_type": "str",
        "location": "str",
        "manufacturer": "str",
        "serial_number": "str",
        "installation_date": "str",
        "warranty_end_date": "str"
    },
    "Functional_Location": {
        "functional_location_id": "int",
        "functional_location_name": "str",
        "location": "str",
        "parent_functional_location": "str",
        "equipment_id": "int",
        "category": "str"
    },
    "Maintenance_Order": {
        "maintenance_order_id": "int",
        "equipment_id": "int",
        "functional_location_id": "int",
        "maintenance_type": "str",
        "priority": "str",
        "order_status": "str",
        "planned_start_date": "str",
        "planned_end_date": "str",
        "actual_start_date": "str",
        "actual_end_date": "str"
    },
    "Maintenance_Notification": {
        "notification_id": "int",
        "equipment_id": "int",
        "functional_location_id": "int",
        "notification_type": "str",
        "created_date": "str",
        "status": "str",
        "description": "str",
        "priority": "str"
    },
    "Project_Definition": {
        "project_id": "int",
        "project_name": "str",
        "project_type": "str",
        "start_date": "str",
        "end_date": "str",
        "status": "str",
        "budget": "float",
        "currency": "str"
    },
    "Work_Breakdown_Structure": {
        "wbs_id": "int",
        "project_id": "int",
        "wbs_name": "str",
        "start_date": "str",
        "end_date": "str",
        "status": "str",
        "budget": "float",
        "currency": "str"
    },
    "Network": {
        "network_id": "int",
        "project_id": "int",
        "network_name": "str",
        "start_date": "str",
        "end_date": "str",
        "status": "str"
    },
    "Activity": {
        "activity_id": "int",
        "network_id": "int",
        "wbs_id": "int",
        "activity_name": "str",
        "activity_type": "str",
        "start_date": "str",
        "end_date": "str",
        "duration": "float",
        "unit_of_duration": "str",
        "status": "str"
    },
    "Cost_Planning": {
        "cost_plan_id": "int",
        "project_id": "int",
        "wbs_id": "int",
        "activity_id": "int",
        "cost_element": "str",
        "planned_cost": "float",
        "actual_cost": "float",
        "currency": "str",
        "status": "str"
    }
}


data_structures_key = "DType"
data_storage_key = "DStorage"


for data_structure, key_values in data_structures.items():
    for field, data_type in key_values.items():
        redis_client.hset(f"{data_structures_key}:{data_structure}", field, data_type)
        redis_client.hset(f"{data_storage_key}:{data_structure}", field, []])

# Retrieve and print the storage fields for each data structure from Redis
for data_structure in data_structures.keys():
    owned_data_fields = redis_client.hkeys(f"{data_storage_key}:{data_structure}")
    owned_data_fields_str = ', '.join([k.decode('utf-8') for k in owned_data_fields])
    print(f"{data_structure}: {owned_data_fields_str}")