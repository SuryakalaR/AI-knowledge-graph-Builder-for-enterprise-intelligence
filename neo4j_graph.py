from neo4j import GraphDatabase

# Neo4j connection details
uri = "bolt://127.0.0.1:7687"
username = "neo4j"
password = "123456789"   

# #Create driverd
driver = GraphDatabase.driver(uri, auth=(username, password))

# Test connection
def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 'CONNECTED TO NEO4J' AS msg")
        for record in result:
            print(record["msg"])

test_connection()

# Define triples
triples = [
    ("Alice", "STUDIES", "DBMS"),
    ("DBMS", "TAUGHT_BY", "Kumar"),
    ("Kumar", "WORKS_IN", "Computer Science")
]

# Clear old data (optional but recommended)
def clear_database():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        print("Database cleared")

clear_database()

# Store triples
def store_triples(triples):
    with driver.session() as session:
        for head, relation, tail in triples:
            session.run(
                f"""
                MERGE (h:Entity {{name: $head}})
                MERGE (t:Entity {{name: $tail}})
                MERGE (h)-[:{relation}]->(t)
                """,
                head=head,
                tail=tail
            )

store_triples(triples)
print("Multi-node graph created successfully")

# Validate graph
def validate_graph():
    with driver.session() as session:
        result = session.run(
            "MATCH (a)-[r]->(b) RETURN a.name, type(r), b.name"
        )
        print("\n--- GRAPH CONTENT ---")
        for record in result:
            print(record)

validate_graph()

# Close driver
driver.close()
