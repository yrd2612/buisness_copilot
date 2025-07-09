from agent.neo4j_setup import connect_neo4j

# Initialize Neo4j connection

'''
Tool output is Accessing database with query: Check if any Raj Paper Mills have balance 50000
parameter: {'name': 'Raj Paper Mills', 'query_type': 'read', 'amount': '50000', 'node_type': 'customer'} and type is <class 'str'>'''
def perform_db_actions(parameter: dict):
    _driver = connect_neo4j().driver
    if parameter['query_type'] == 'read':
        query = f"MATCH (n:{parameter['node_type']} {{name: '{parameter['name']}'}}) RETURN n"
        with _driver.session() as session:
            results = session.run(query).data()
            print("DB Results are",results)
            if results:
                if parameter["comparison"] == "equal_to":
                    if results[0]['n']['balance'] == parameter['amount']:
                        print("DB Results:")
                        return(f"Yes {parameter['name']} has balance {parameter['amount']}")
                    else:
                        print("DB Results:")
                        print(f"{parameter['name']} does not have balace {parameter['amount']}") 
                        return(f"{parameter['name']} does not have balace {parameter['amount']}")   



    return True

