import streamlit as st
from src.pdf_loader import load_and_index_pdfs
from src.rag import process_query

st.set_page_config(page_title="RAG PDF Pro", layout="wide")

st.title("📄 RAG PDF Pro — Perguntas e respostas em PDFs com IA")

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# Sidebar ---------------------------------------------------
st.sidebar.header("📁 Carregar PDFs")

uploaded_files = st.sidebar.file_uploader(
    "Envie um ou vários PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    with st.spinner("Processando e indexando PDFs..."):
        st.session_state.vectorstore = load_and_index_pdfs(uploaded_files)

    st.success("PDFs processados com sucesso!")

st.markdown("---")

# Pergunta ---------------------------------------------------
pergunta = st.text_input("🔎 Pergunta sobre os PDFs:")

if st.button("Enviar pergunta"):
    if not st.session_state.vectorstore:
        st.error("Nenhum PDF carregado.")
    else:
        resposta, fontes = process_query(pergunta, st.session_state.vectorstore)

        st.subheader("🧠 Resposta")
        st.write(resposta)

        st.subheader("📌 Fontes utilizadas")
        for f in fontes:
            st.write(f"**{f['pdf']}**")
            st.write(f["texto"] + "\n---")
