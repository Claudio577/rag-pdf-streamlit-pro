import streamlit as st
from src.pdf_loader import load_and_index_pdfs
from src.rag import process_query

st.set_page_config(page_title="RAG PDF Pro", layout="wide")

# ============================
# DESCRIÇÃO DO SISTEMA
# ============================

st.markdown("""
### 📘 O que este sistema faz

Este aplicativo utiliza **Inteligência Artificial + LangChain moderno** para analisar PDFs e responder perguntas com base no conteúdo real dos documentos.

Ele é construído com **RAG profissional**, utilizando:
- FAISS + embeddings → busca inteligente  
- GPT-4o-mini → respostas contextualizadas  
- LangChain moderno → pipeline atualizado  
- Resumo completo do PDF com 1 clique  

Este sistema **não inventa informações**: responde somente com base no conteúdo do PDF.
""")

# ============================
# ESTADO INICIAL
# ============================

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = []

# ============================
# SIDEBAR — UPLOAD + RESUMO
# ============================

st.sidebar.header("📁 Carregar PDFs")

uploaded_files = st.sidebar.file_uploader(
    "Envie um ou vários PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

# Processar PDFs
if uploaded_files is not None and len(uploaded_files) > 0:

    st.session_state.pdf_bytes = [f.getvalue() for f in uploaded_files]

    with st.spinner("Processando e indexando PDFs..."):
        st.session_state.vectorstore = load_and_index_pdfs(st.session_state.pdf_bytes)

    st.success("PDFs processados com sucesso!")


# 🔽 BOTÃO DE RESUMO COMPLETO (NA SIDEBAR)
st.sidebar.markdown("---")
if st.sidebar.button("📄 Gerar resumo completo do PDF"):
    if not st.session_state.vectorstore:
        st.sidebar.error("Nenhum PDF carregado.")
    else:
        resumo, fontes = process_query("RESUMO_COMPLETO_PDF", st.session_state.vectorstore)

        st.subheader("🧠 Resumo completo do PDF")
        st.write(resumo)

        st.subheader("📌 Fontes utilizadas")
        for f in fontes:
            st.write(f"**{f['pdf']}**")
            st.write(f["texto"] + "\n---")

# ============================
# PERGUNTA NORMAL
# ============================

st.markdown("---")
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
