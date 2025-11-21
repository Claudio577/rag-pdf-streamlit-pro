import streamlit as st
from src.pdf_loader import load_and_index_pdfs
from src.rag import process_query

st.set_page_config(page_title="RAG PDF Pro", layout="wide")

st.title(" RAG PDF Pro — Perguntas e respostas em PDFs com IA")
st.info("""
### 📘 O que este sistema faz

Este aplicativo utiliza **Inteligência Artificial + LangChain moderno** para analisar PDFs e responder perguntas com base no conteúdo real dos documentos.

Ele é construído com um modelo de RAG (*Retrieval Augmented Generation*) no estilo **sistemas profissionais**, utilizando:

- LangChain moderno + RAG simples e eficiente
- Busca inteligente de trechos relevantes (FAISS + embeddings)
- Análise profunda com IA (GPT-4o-mini)
- Respostas explicadas, resumidas e contextualizadas
- Geração de **resumos completos** do PDF com um único clique

Este não é um ChatGPT comum.  
Ele **não inventa informações**: responde apenas com base no conteúdo real do PDF.

Ideal para:
- Portarias  
- Resoluções  
- Leis  
- Documentos técnicos  
- Contratos  
- Regimentos  
- Normas administrativas  

Use o campo de perguntas para dúvidas específicas ou marque a opção  
**"Fazer resumo completo do PDF"** para uma visão geral.
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
st.sidebar.header("Carregar PDFs")

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
fazer_resumo = st.checkbox("Fazer resumo completo do PDF")


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
