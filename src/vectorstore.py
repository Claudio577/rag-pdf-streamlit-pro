from langchain_community.vectorstores import FAISS
from src.embeddings import get_embeddings

def build_vectorstore(docs):
    embeddings = get_embeddings()

    if not docs:
        raise ValueError("Nenhum documento válido foi extraído dos PDFs.")

    try:
        vectorstore = FAISS.from_documents(docs, embeddings)
    except Exception as e:
        raise RuntimeError(f"Erro ao criar FAISS: {str(e)}")

    if vectorstore is None:
        raise RuntimeError("FAISS retornou None. Índice não foi criado.")

    return vectorstore
