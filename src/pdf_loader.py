import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.preprocess import remove_governo_headers, clean_text_block
from src.vectorstore import build_vectorstore

def load_and_index_pdfs(uploaded_files):
    """Carrega, limpa, divide e indexa PDFs em um vectorstore FAISS."""

    all_docs = []

    for pdf in uploaded_files:
        temp_path = f"temp_{pdf.name}"

        # grava o PDF temporariamente
        with open(temp_path, "wb") as f:
            f.write(pdf.getbuffer())

        loader = PyPDFLoader(temp_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=120
        )
        docs = splitter.split_documents(docs)

        # limpeza e normalização
        for d in docs:
            texto = remove_governo_headers(d.page_content)
            texto = clean_text_block(texto)
            d.page_content = "passage: " + texto
            d.metadata["pdf_name"] = pdf.name

        all_docs.extend(docs)

        # ❗❗❗ REMOVIDO: não apagar o arquivo no Streamlit Cloud
        # os.remove(temp_path)

    return build_vectorstore(all_docs)
