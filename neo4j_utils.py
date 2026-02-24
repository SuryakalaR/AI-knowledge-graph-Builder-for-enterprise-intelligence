import streamlit as st
from neo4j import GraphDatabase

URI = st.secrets["NEO4J_URI"]
USER = st.secrets["NEO4J_USER"]
PASSWORD = st.secrets["NEO4J_PASSWORD"]

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def get_student_count():
    with driver.session() as session:
        result = session.run("MATCH (s:Student) RETURN count(s) AS total")
        return result.single()["total"]
