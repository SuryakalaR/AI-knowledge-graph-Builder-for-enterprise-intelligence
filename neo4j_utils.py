from neo4j import GraphDatabase

URI = "bolt://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "123456789"  # change if needed

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def get_student_count():
    with driver.session() as session:
        result = session.run("MATCH (s:Student) RETURN count(s) AS total")
        return result.single()["total"]
