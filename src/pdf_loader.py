import tempfile
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.preprocess import remove_governo_headers, clean_text_block
from src.vectorstore import build_vectorstore

@st.cache_resource
def load_and_index_pdfs(pdf_bytes_list):
    """
    Recebe uma lista de bytes de PDFs.
    Cria arquivos temporários.
    Extrai texto.
    Constrói um vectorstore FAISS.
    """

    all_docs = []

    for i, pdf_bytes in enumerate(pdf_bytes_list):
        # Criar PDF temporário a partir de bytes
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_bytes)
            temp_path = tmp.name

        pdf_name = f"PDF_{i+1}.pdf"

        loader = PyPDFLoader(temp_path)
        raw_docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=120
        )
        docs = splitter.split_documents(raw_docs)

        for d in docs:
            texto = remove_governo_headers(d.page_content)
            texto = clean_text_block(texto)
            d.page_content = "passage: " + texto
            d.metadata["pdf_name"] = pdf_name

        all_docs.extend(docs)

    if not all_docs:
        raise ValueError("Nenhum texto foi extraído dos PDFs enviados.")

    return build_vectorstore(all_docs)

