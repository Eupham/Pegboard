import redis
import datetime
from redisgraph import Graph

class LedgerGraph:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db)
        self.graph = Graph("ledger", self.redis)
        self._create_nodes()

    def _create_nodes(self):
        module_query = "MERGE (:Module {name: 'ledger'})"
        self.graph.query(module_query)
        props = [("date", "date_accrued"),]
        attrs = [("type",), ("accrued_bool",), ("amount",)]
        metadata = [("id",), ("description",)]

        for prop in props:
            prop_query = f"MATCH (m:Module {{name: 'ledger'}}) MERGE (m)-[:HAS_PROPERTY]->(:Property {{name: '{prop[0]}'}})"
            self.graph.query(prop_query)

        for attr in attrs:
            attr_query = f"MATCH (m:Module {{name: 'ledger'}}) MERGE (m)-[:HAS_ATTRIBUTE]->(:Attribute {{name: '{attr[0]}'}})"
            self.graph.query(attr_query)

        for meta in metadata:
            meta_query = f"MATCH (m:Module {{name: 'ledger'}}) MERGE (m)-[:HAS_METADATA]->(:Metadata {{name: '{meta[0]}'}})"
            self.graph.query(meta_query)


    def add_line(self, date, date_accrued, line_type, accrued_bool, amount, line_id, description):
        query = "MATCH (m:Module {name: $module_name}) CREATE (m)-[:HAS_LINE]->(line:Line {date: $date, date_accrued: $date_accrued, type: $line_type, accrued_bool: $accrued_bool, amount: $amount, id: $line_id, description: $description})"
        params = {"module_name": "ledger", "date": date, "date_accrued": date_accrued, "line_type": line_type, "accrued_bool": accrued_bool, "amount": amount, "line_id": line_id, "description": description}
        self.graph.query(query, params)
    
    def remove_line(self, line_id):
        query = "MATCH (m:Module {name: $module_name})-[:HAS_LINE]->(line:Line {id: $line_id}) DETACH DELETE line"
        params = {"module_name": "ledger", "line_id": line_id}
        self.graph.query(query, params)

    def get_all_lines(self):
        query = "MATCH (m:Module {name: 'ledger'})-[:HAS_LINE]->(line:Line) RETURN line.date, line.date_accrued, line.type, line.accrued_bool, line.amount, line.id, line.description"
        result = self.graph.query(query)
        return [record for record in result.result_set]

    def s_lines(self, property_name, property_value):
        query = "MATCH (m:Module {name: 'ledger'})-[:HAS_LINE]->(line:Line {%s: $value}) RETURN line.date, line.date_accrued, line.type, line.accrued_bool, line.amount, line.id, line.description" % property_name
        params = {"value": property_value}
        result = self.graph.query(query, params)
        return [record for record in result.result_set]
    
    def range_s_dates(self, start_date, end_date):
        query = "MATCH (m:Module {name: 'ledger'})-[:HAS_LINE]->(line:Line) WHERE line.date >= $start_date AND line.date <= $end_date RETURN line.date, line.date_accrued, line.type, line.accrued_bool, line.amount, line.id, line.description"
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date().isoformat()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date().isoformat()
        params = {"start_date": start_date, "end_date": end_date}
        result = self.graph.query(query, params)
        return [record for record in result.result_set]
    
    def sum_results(self, results):
        total = 0
        for r in results:
            total += r[4]
        return total


if __name__ == '__main__':    
    ledger = LedgerGraph()
    ledger.add_line('2023-05-05', '2023-05-05', 'expense', False, 100, 'line1', 'description1')
    ledger.add_line('2023-05-05', '2023-05-05', 'expense', False, 100, 'line2', 'description1')

    print(ledger.get_all_lines())
    results = ledger.s_lines('date', '2023-05-05')
    print(results)
    results = ledger.range_s_dates('2023-05-04', '2023-05-06')
    print(results)
    total = ledger.sum_results(results)
    print(total)
    ledger.remove_line('line1')
    print(ledger.get_all_lines())
