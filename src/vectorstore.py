from langchain_community.vectorstores import FAISS
from src.embeddings import get_embeddings

def build_vectorstore(docs):
    embeddings = get_embeddings()
    return FAISS.from_documents(docs, embeddings)
