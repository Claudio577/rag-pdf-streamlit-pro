from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.preprocess import remove_governo_headers, clean_text_block
from src.vectorstore import build_vectorstore
import tempfile

def load_and_index_pdfs(uploaded_files):
    """Carrega, limpa e indexa PDFs usando byte-stream (compatível com Streamlit Cloud)."""

    all_docs = []

    for pdf in uploaded_files:
        # Criar arquivo temporário seguro
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf.getbuffer())
            temp_path = tmp.name

        loader = PyPDFLoader(temp_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=120
        )
        docs = splitter.split_documents(docs)

        for d in docs:
            texto = remove_governo_headers(d.page_content)
            texto = clean_text_block(texto)
            d.page_content = "passage: " + texto
            d.metadata["pdf_name"] = pdf.name

        all_docs.extend(docs)

    # Garantir que exista conteúdo
    if not all_docs:
        raise ValueError("Nenhum conteúdo foi extraído dos PDFs. Verifique o arquivo enviado.")

    return build_vectorstore(all_docs)

