from neo4j import GraphDatabase
import pandas as pd
import networkx as nx

# 🔑 UPDATE YOUR PASSWORD HERE
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "123456789"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


def fetch_student_data():
    query = """
    MATCH (s:Student)-[:STUDIES_IN]->(d:Department)
    MATCH (s)-[:TAUGHT_BY]->(t:Teacher)
    RETURN s.name AS name,
           s.age AS age,
           s.marks AS marks,
           s.cgpa AS cgpa,
           d.name AS department,
           t.name AS teacher
    """

    with driver.session() as session:
        result = session.run(query)
        data = [record.data() for record in result]

    return pd.DataFrame(data)


def fetch_graph_data(department=None):

    G = nx.Graph()

    with driver.session() as session:

        if department and department != "All":

            query = """
            MATCH (s:Student)-[:STUDIES_IN]->(d:Department {name:$dept})
            MATCH (s)-[:TAUGHT_BY]->(t:Teacher)
            RETURN s.name AS student,
                   d.name AS department,
                   t.name AS teacher
            """

            result = session.run(query, dept=department)

        else:

            query = """
            MATCH (s:Student)-[:STUDIES_IN]->(d:Department)
            MATCH (s)-[:TAUGHT_BY]->(t:Teacher)
            RETURN s.name AS student,
                   d.name AS department,
                   t.name AS teacher
            """

            result = session.run(query)

        for record in result:
            s = record["student"]
            d = record["department"]
            t = record["teacher"]

            G.add_edge(s, d)
            G.add_edge(s, t)

    return G
