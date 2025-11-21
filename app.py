import streamlit as st
from src.pdf_loader import load_and_index_pdfs
from src.rag import process_query

st.set_page_config(page_title="RAG PDF Pro", layout="wide")

st.title(" RAG PDF Pro — Perguntas e respostas em PDFs com IA")
st.markdown("""
### 📘 Sobre o sistema  
Este aplicativo utiliza Inteligência Artificial para **ler, analisar e responder perguntas** com base no conteúdo real de PDFs enviados por você.  
Ele funciona com tecnologia *RAG* (Retrieval Augmented Generation), que:
- 📂 localiza automaticamente trechos relevantes no PDF  
- 🧠 combina essas informações com um modelo de IA  
- ✍️ gera respostas precisas, explicações claras ou resumos completos  

Você pode fazer perguntas específicas ou ativar o **Resumo completo do PDF** para obter uma visão geral estruturada.
""")


# ============================
# ESTADO INICIAL
# ============================
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = []


# ============================
# SIDEBAR — UPLOAD
# ============================
st.sidebar.header("📁 Carregar PDFs")

uploaded_files = st.sidebar.file_uploader(
    "Envie um ou vários PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

# Processar PDFs somente quando realmente houver arquivos
if uploaded_files is not None and len(uploaded_files) > 0:

    # Guardar conteúdo dos PDFs como bytes
    st.session_state.pdf_bytes = [f.getvalue() for f in uploaded_files]

    with st.spinner("Processando e indexando PDFs..."):
        st.session_state.vectorstore = load_and_index_pdfs(st.session_state.pdf_bytes)

    st.success("PDFs processados com sucesso!")

st.markdown("---")


# ============================
# CAMPO DE PERGUNTA
# ============================
pergunta = st.text_input("🔎 Pergunta sobre os PDFs:")

# Checkbox para resumo completo
fazer_resumo = st.checkbox("📄 Fazer resumo completo do PDF")


# ============================
# EXECUTAR CONSULTA
# ============================
if st.button("Enviar pergunta"):
    if not st.session_state.vectorstore:
        st.error("Nenhum PDF carregado.")
    else:

        # Caso o usuário queira resumo completo
        if fazer_resumo:
            pergunta = (
                "Faça um resumo completo, detalhado e estruturado do PDF inteiro, "
                "destacando objetivos, contexto legal, regras, obrigações, prazos, "
                "responsabilidades e os principais pontos tratados no documento."
            )

        # Executar RAG
        resposta, fontes = process_query(pergunta, st.session_state.vectorstore)

        # Mostrar resposta
        st.subheader("🧠 Resposta")
        st.write(resposta)

        # Mostrar trechos usados
        st.subheader("📌 Fontes utilizadas")
        for f in fontes:
            st.write(f"**{f['pdf']}**")
            st.write(f["texto"] + "\n---")
