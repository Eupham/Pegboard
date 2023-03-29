import redis
from redisgraph import Graph
from treelib import Node, Tree

class ContinentTree:
    def __init__(self):
        self.redis_db = redis.Redis(host='localhost', port=6379)
        self.graph = Graph('mygraph', self.redis_db)
        self.tree = Tree()
        self.continent_nodes = []
        self.create_tree()

    def create_tree(self):
        root = Node('Globe')
        self.graph.query("CREATE (:Node {name: 'Globe'})")
        self.tree.add_node(root)
        self.create_continents(root)
        self.create_nations()

    def create_continents(self, root):
        continents = ["North America", "Europe", "Asia", "South America", "Africa", "Oceania"]
        for continent in continents:
            continent_node = Node(continent)
            self.graph.query(f"MATCH (n:Node {{name: 'Globe'}}) CREATE (n)-[:HAS_CHILD]->(:Node {{name: '{continent}'}})")
            self.tree.add_node(continent_node, root.identifier)
            self.continent_nodes.append(continent_node)

    def create_nations(self):
        nations = {
    "North America": ["Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada", "Costa Rica", "Cuba", "Dominica", "Dominican Republic", "El Salvador", "Grenada", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Trinidad and Tobago", "United States of America (USA)"],
    "Europe": ["Albania", "Andorra", "Armenia", "Austria", "Azerbaijan", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Macedonia (FYROM)", "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Russia", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom (UK)", "Vatican City (Holy See)"],
    "Asia": ["Afghanistan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China", "East Timor", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar (Burma)", "Nepal", "North Korea", "Oman", "Pakistan", "Palestine", "Philippines", "Qatar", "Russia", "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria", "Taiwan", "Tajikistan", "Thailand", "Turkey", "Turkmenistan", "United Arab Emirates (UAE)", "Uzbekistan", "Vietnam", "Yemen"],
    "South America": ["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay", "Peru", "Suriname", "Uruguay", "Venezuela"],
    "Africa": ["Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Cape Verde", "Central African Republic", "Chad", "Comoros", "Congo, Democratic Republic of the", "Congo, Republic of the", "Cote d\\'Ivoire", "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Swaziland", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"],
    "Oceania": ["Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia", "Nauru", "New Zealand", "Palau", "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu"]
}
        for continent, nation_list in nations.items():
            for nation in nation_list:
                node = Node(nation)
                parent_node = next(node for node in self.continent_nodes if node.tag == continent)
                self.graph.query(f"MATCH (n:Node {{name: '{continent}'}}) CREATE (n)-[:HAS_CHILD]->(:Node {{name: '{nation}'}})")
                self.tree.add_node(node, parent_node.identifier)

    def create_nation_children(self, nation, children_dict):
        node = next(node for node in self.tree.all_nodes() if node.tag == nation)
        for category, specifics in children_dict.items():
            category_node = Node(category)
            self.graph.query(f"MATCH (n:Node {{name: '{nation}'}}) CREATE (n)-[:HAS_CHILD]->(:Node {{name: '{category}'}})")
            self.tree.add_node(category_node, node.identifier)
            for specific in specifics:
                specific_node = Node(specific)
                self.graph.query(f"MATCH (n:Node {{name: '{category}'}}) CREATE (n)-[:HAS_CHILD]->(:Node {{name: '{specific}'}})")
                self.tree.add_node(specific_node, category_node.identifier)

    def print_tree(self):
        self.tree.show()

if __name__ == "__main__":
    continent_tree = ContinentTree()
    children_dict = {
    "Government": ["The White House", "United States Congress"],
    "Foundations": ["Bill gates foundation"],
    "Universities": ["Harvard University", "Massachusetts Institute of Technology"]
}
    continent_tree.create_nation_children("United States of America (USA)", children_dict)

    continent_tree.print_tree()
