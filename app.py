
import streamlit as st
from neo4j_utils import get_student_count
from rag_utils import semantic_search

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="College Knowledge Graph + RAG",
    layout="wide"
)

# ----------------------------
# Custom Styling
# ----------------------------
# ----------------------------
# Custom CSS Styling
# ----------------------------
# ---------- Custom Styling ----------
st.set_page_config(page_title="College KG + RAG", layout="wide")

st.markdown("""
<style>

/* Metric Value Color */
div[data-testid="metric-container"] {
    background-color: #1e293b;
    border: 2px solid #00f5d4;
    padding: 15px;
    border-radius: 15px;
}

/* THIS FIXES THE NUMBER COLOR */
div[data-testid="metric-container"] > div {
    color: #ffffff !important;
    font-size: 32px !important;
    font-weight: bold;
}

/* Specifically target metric number */
div[data-testid="stMetricValue"] {
    color: #ffdd00 !important;
    font-size: 36px !important;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)




# ----------------------------
# Title
# ----------------------------
st.markdown("<h1 style='text-align:center;'>🎓 College Knowledge Graph + RAG System</h1>", unsafe_allow_html=True)

st.divider()

# ----------------------------
# Neo4j Section
# ----------------------------
st.header("📊 Graph Data")

count = get_student_count()

col1, col2 = st.columns(2)
col1.metric("👩‍🎓 Total Students", count)

st.divider()

# ----------------------------
# RAG Section
# ----------------------------
st.header("🤖 Ask a Question")

query = st.text_input("Enter your question about students, departments, teachers...")

if query:
    with st.spinner("Searching intelligently... 🔍"):
        result = semantic_search(query)
    
    st.success("Relevant Information Found ✅")
    st.write(result)
