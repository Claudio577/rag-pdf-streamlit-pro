import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.preprocess import remove_governo_headers, clean_text_block
from src.vectorstore import build_vectorstore

def load_and_index_pdfs(uploaded_files):
    """Carrega PDFs em memória e cria um vectorstore FAISS seguro."""

    all_docs = []

    for pdf in uploaded_files:
        # Criar arquivo temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf.getbuffer())
            temp_path = tmp.name

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
            d.metadata["pdf_name"] = pdf.name

        all_docs.extend(docs)

    if not all_docs:
        raise ValueError("Nenhum texto foi extraído. PDF está vazio ou inválido.")

    return build_vectorstore(all_docs)

