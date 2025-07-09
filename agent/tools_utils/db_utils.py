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
            if parameter["comparison"]!= "Not Applicable":
                if parameter["comparison"] == "equal_to":
                    if results[0]['n']['balance'] == parameter['amount']:
                        print("DB Results:")
                        return(f"Yes {parameter['name']} has balance {parameter['amount']}")
                    else:
                        print("DB Results:")
                        print(f"{parameter['name']} does not have balace {parameter['amount']}") 
                        return(f"{parameter['name']} does not have balace {parameter['amount']}")  
                elif parameter["comparison"] == "greater_than":
                    if results[0]['n']['balance'] > parameter['amount']:
                        print("DB Results:")
                        return(f"Yes {parameter['name']} has balance greater than {parameter['amount']}")
                    else:
                        print("DB Results:")
                        print(f"{parameter['name']} does not have balance greater than {parameter['amount']}") 
                        return(f"{parameter['name']} does not have balance greater than {parameter['amount']}")
                elif parameter["comparison"] == "less_than":
                    if results[0]['n']['balance'] < parameter['amount']:
                        print("DB Results:")
                        return(f"Yes {parameter['name']} has balance less than {parameter['amount']}")
                    else:
                        print("DB Results:")
                        print(f"{parameter['name']} does not have balance less than {parameter['amount']}") 
                        return(f"{parameter['name']} does not have balance less than {parameter['amount']}") 
                elif parameter["comparison"] == "not_equal_to":
                    if results[0]['n']['balance'] != parameter['amount']:
                        print("DB Results:")
                        return(f"Yes {parameter['name']} has balance not equal to {parameter['amount']}")
                    else:
                        print("DB Results:")
                        print(f"{parameter['name']} has balance equal to {parameter['amount']}") 
                        return(f"{parameter['name']} has balance equal to {parameter['amount']}")
            else:
                if results:
                    print("DB Results:")
                    return(f"The records for  {parameter['name']} are {results[0]['n']['balance']}")
                else:
                    print("DB Results:")
                    return(f"No {parameter['name']} found in the database")
    else:
        query = f"CREATE (n:{parameter['node_type']} {{name: '{parameter['name']}', balance: {parameter['amount']}}})"
        with _driver.session() as session:
            session.run(query)
            print("DB Results:")
            print(f"Created {parameter['node_type']} node with name {parameter['name']} and balance {parameter['amount']}")



    return True

