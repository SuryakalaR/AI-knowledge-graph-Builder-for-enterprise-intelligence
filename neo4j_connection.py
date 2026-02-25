from neo4j import GraphDatabase

URI = "bolt://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "123456789"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def get_driver():
    return driver
