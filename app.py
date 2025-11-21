import streamlit as st
from src.pdf_loader import load_and_index_pdfs
from src.rag import process_query

# ----------------------------
# CONFIGURAÇÃO DO APP
# ----------------------------
st.set_page_config(page_title="RAG PDF Pro", layout="wide")

st.markdown("""
### 📘 O que este sistema faz

Este aplicativo utiliza **Inteligência Artificial + LangChain moderno** para analisar PDFs e responder perguntas com base no conteúdo real dos documentos.

Ele é construído com um modelo de RAG (*Retrieval Augmented Generation*) no estilo **sistemas profissionais**, utilizando:

- 🔍 Busca inteligente de trechos relevantes (FAISS + Embeddings)
- 🤖 Análise profunda com IA (GPT-4o-mini)
- 🧠 Respostas explicadas, resumidas e contextualizadas
- 📄 Geração de **resumos completos** do PDF com um clique

Este sistema **não inventa informações**: responde somente com base no conteúdo real do PDF.

Ideal para:
- Portarias  
- Resoluções  
- Leis  
- Documentos técnicos  
- Contratos  
- Regimentos  
- Normas administrativas  

Use o campo de perguntas para dúvidas específicas ou clique em  
**“Resumo completo do PDF”** para gerar uma análise completa.
""")

# ----------------------------
# ESTADOS INICIAIS
# ----------------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = []

# Novo estado: controla exibição do resumo
if "modo_resumo" not in st.session_state:
    st.session_state.modo_resumo = False


# ----------------------------
# SIDEBAR — UPLOAD DE PDFs
# ----------------------------
st.sidebar.header("📁 Carregar PDFs")

uploaded_files = st.sidebar.file_uploader(
    "Envie um ou vários PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) > 0:

    # Salvar bytes dos PDFs no estado
    st.session_state.pdf_bytes = [f.getvalue() for f in uploaded_files]

    with st.spinner("Processando e indexando PDFs..."):
        st.session_state.vectorstore = load_and_index_pdfs(st.session_state.pdf_bytes)

    st.success("PDFs processados com sucesso!")

st.markdown("---")


# ----------------------------
# PERGUNTA OU RESUMO
# ----------------------------
pergunta = st.text_input("🔎 Pergunta sobre os PDFs:")

# 1 — Se o usuário clicou anteriormente em "Resumo completo"
if st.session_state.modo_resumo:

    resposta, fontes = process_query("RESUMO_COMPLETO_PDF", st.session_state.vectorstore)

    st.subheader("🧠 Resumo do PDF")
    st.write(resposta)

    st.subheader("📌 Fontes utilizadas")
    for f in fontes:
        st.write(f"**{f['pdf']}**")
        st.write(f["texto"] + "\n---")

    # Após exibir o resumo, permite perguntas novamente
    st.session_state.modo_resumo = False


# 2 — Campo de pergunta está VAZIO → mostra botão de Resumo
elif not pergunta.strip():

    if st.button("📄 Resumo completo do PDF"):
        if not st.session_state.vectorstore:
            st.error("Nenhum PDF carregado.")
        else:
            st.session_state.modo_resumo = True
            st.experimental_rerun()


# 3 — Se usuário digitou pergunta → mostra botão "Enviar pergunta"
else:

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
