from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain.schema import Document

# Sample knowledge
texts = [
    "Dr. Ravi teaches DBMS in CSE department.",
    "Ms. Priya teaches Mathematics in AIML.",
    "Dr. Ravi is HOD of CSE.",
    "Student 1 studies in CSE.",
    "Student 2 studies in AIML."
]

documents = [Document(page_content=text) for text in texts]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.from_documents(documents, embeddings)

def semantic_search(query):
    docs = vectorstore.similarity_search(query, k=2)
    return "\n".join([doc.page_content for doc in docs])
