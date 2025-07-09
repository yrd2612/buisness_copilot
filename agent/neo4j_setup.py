from neo4j import GraphDatabase
import os

class connect_neo4j:
    _driver = None  # Class-level variable to hold the singleton driver
    
    def __init__(self):
        if connect_neo4j._driver is None:
            AURA_CONNECTION_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
            AURA_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
            AURA_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
            connect_neo4j._driver = GraphDatabase.driver(
                AURA_CONNECTION_URI,
                auth=(AURA_USERNAME, AURA_PASSWORD)
            )
        self.driver = connect_neo4j._driver