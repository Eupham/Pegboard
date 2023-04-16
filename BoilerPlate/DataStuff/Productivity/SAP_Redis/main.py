import redis
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView, QTreeView, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox, QListWidget, QWidget, QTableView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Retrieve the module names and table names from Redis
data_structures_dict = {}
for module_key in redis_client.keys('Module:*'):
    module = module_key.decode('utf-8').split(':')[1]
    tables = [table.decode('utf-8') for table in redis_client.smembers(module_key)]
    data_structures_dict[module] = tables

# Create the main window
app = QApplication([])
window = QMainWindow()
window.setWindowTitle('SAP Redis Framework')

# Create the central widget and layout
central_widget = QWidget()
layout = QHBoxLayout()
central_widget.setLayout(layout)

# Create the left-side widget and layout
left_widget = QWidget()
left_layout = QVBoxLayout()
left_widget.setLayout(left_layout)

# Create the module selection combo box and add it to the layout
module_combo_box = QComboBox()
module_combo_box.addItems(data_structures_dict.keys())
left_layout.addWidget(module_combo_box)

# Create the table list widget and add it to the layout
table_list_widget = QListWidget()
left_layout.addWidget(table_list_widget)

# Define the function to display the available tables for a selected module
def display_tables(module_name):
    table_names = data_structures_dict[module_name]
    table_list_widget.clear()
    table_list_widget.addItems(table_names)

# Connect the currentTextChanged signal of the combo box to the display_tables function
module_combo_box.currentTextChanged.connect(display_tables)

# Create the right-side widget and layout
right_widget = QWidget()
right_layout = QVBoxLayout()
right_widget.setLayout(right_layout)

# Create the tree view and add it to the layout
tree_view = QTreeView()
tree_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
tree_view.setHeaderHidden(True)
tree_view.header().setSectionResizeMode(QHeaderView.ResizeToContents)
tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
right_layout.addWidget(tree_view)

# Define the function to display the selected data structure in the tree view and table view
def display_data_structure(data_structure_name):
    data_structure = redis_client.hgetall(f"DType:{data_structure_name}")

    # Define the model for the tree view
    model = QStandardItemModel()
    for field, data_type in data_structure.items():
        item = QStandardItem(field.decode('utf-8'))
        item.setEditable(False)
        model.appendRow(item)
        sub_item = QStandardItem(data_type.decode('utf-8'))
        sub_item.setEditable(False)
        item.appendRow(sub_item)
    tree_view.setModel(model)

    # Define the model for the table view
    table_model = QStandardItemModel()
    table_model.setHorizontalHeaderLabels(['Key', 'Value'])

    for key, value in redis_client.hgetall(f"DStorage:{data_structure_name}").items():
        key_item = QStandardItem(key.decode('utf-8'))
        value_item = QStandardItem(value.decode('utf-8'))
        table_model.appendRow([key_item, value_item])

    # Transpose the table model
    table_model_transposed = QStandardItemModel()
    table_model_transposed.setHorizontalHeaderLabels(['Field', 'Value'])
    for row in range(table_model.rowCount()):
        key_item = table_model.item(row, 0).clone()
        value_item = table_model.item(row, 1).clone()
        table_model_transposed.appendRow([key_item, value_item])

    # Create the table view and add it to the right-side layout
    table_view = QTableView()
    table_view.setModel(table_model_transposed)
    table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
    table_view.horizontalHeader().setStretchLastSection(True)  # Stretch the last column to fill the space
    right_layout.addWidget(table_view)

# Connect the itemClicked signal of the table list widget to the display_data_structure function
table_list_widget.itemClicked.connect(lambda item: display_data_structure(item.text()))

# Add the left-side and right-side widgets to the main layout
layout.addWidget(left_widget)
layout.addWidget(right_widget)

# Show the window
window.setCentralWidget(central_widget)
window.show()
app.exec_()