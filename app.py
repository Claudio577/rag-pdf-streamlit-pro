import streamlit as st
from src.pdf_loader import load_and_index_pdfs
from src.rag import process_query

st.set_page_config(page_title="RAG PDF Pro", layout="wide")

# -------------------------------------------------------
# ESTILIZAÇÃO
# -------------------------------------------------------
st.markdown("""
<style>
    .main-title { font-size: 32px; font-weight: 700; margin-top: 10px; }
    .section-title { font-size: 22px; font-weight: 600; margin-top: 30px; }
    .response-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f7f7f7;
        border: 1px solid #ddd;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# ESTADOS
# -------------------------------------------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = []

if "resumo_pdf" not in st.session_state:
    st.session_state.resumo_pdf = None

# controla se o resumo está aberto na tela
if "mostrar_resumo" not in st.session_state:
    st.session_state.mostrar_resumo = False


# -------------------------------------------------------
# SIDEBAR — UPLOAD
# -------------------------------------------------------
st.sidebar.header("📁 Carregar PDFs")

uploaded_files = st.sidebar.file_uploader(
    "Envie um ou vários PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    st.session_state.pdf_bytes = [f.getvalue() for f in uploaded_files]

    with st.spinner("Processando PDFs..."):
        st.session_state.vectorstore = load_and_index_pdfs(st.session_state.pdf_bytes)

    st.sidebar.success("PDFs carregados com sucesso!")

st.sidebar.markdown("---")


# -------------------------------------------------------
# BOTÃO DE RESUMO COMPLETO DO PDF (FICA NA SIDEBAR)
# -------------------------------------------------------
if st.sidebar.button("📄 Gerar resumo completo do PDF"):
    if not st.session_state.vectorstore:
        st.sidebar.error("Nenhum PDF carregado.")
    else:
        resumo, fontes = process_query("RESUMO_COMPLETO_PDF", st.session_state.vectorstore)
        st.session_state.resumo_pdf = (resumo, fontes)
        st.session_state.mostrar_resumo = True


# -------------------------------------------------------
# ÁREA PRINCIPAL — TÍTULO E EXPLICAÇÃO
# -------------------------------------------------------
st.markdown("<div class='main-title'>📄 RAG PDF Pro — Perguntas e Respostas Inteligentes</div>", unsafe_allow_html=True)

st.markdown("""
Este sistema usa **RAG + LangChain moderno** para analisar seus PDFs e fornecer:

- Resumo completo do documento  
- Respostas exatas baseadas no conteúdo real  
- Zero alucinação  
- Busca de alta precisão  

Ideal para portarias, resoluções, leis, contratos e documentos oficiais.
""")


# -------------------------------------------------------
# MOSTRAR O RESUMO (SE EXISTE E ESTÁ ABERTO)
# -------------------------------------------------------
if st.session_state.resumo_pdf and st.session_state.mostrar_resumo:

    resumo, fontes = st.session_state.resumo_pdf

    st.markdown("<div class='section-title'>📘 Resumo completo do PDF</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='response-box'>{resumo}</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>📌 Fontes utilizadas</div>", unsafe_allow_html=True)
    for f in fontes:
        st.markdown(f"""
        **{f['pdf']}**  
        <div class='response-box'>{f['texto']}</div>
        """, unsafe_allow_html=True)

    # BOTÃO DE FECHAR RESUMO
    if st.button("Fechar resumo"):
        st.session_state.mostrar_resumo = False


st.markdown("---")


# -------------------------------------------------------
# PERGUNTA NORMAL
# -------------------------------------------------------
st.markdown("<div class='section-title'>🔎 Pergunta sobre os PDFs</div>", unsafe_allow_html=True)
pergunta = st.text_input("Digite sua pergunta:")

if st.button("Enviar pergunta"):
    if not st.session_state.vectorstore:
        st.error("Nenhum PDF carregado.")
    else:
        resposta, fontes = process_query(pergunta, st.session_state.vectorstore)

        st.markdown("<div class='section-title'>🧠 Resposta</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='response-box'>{resposta}</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>📌 Fontes utilizadas</div>", unsafe_allow_html=True)
        for f in fontes:
            st.markdown(f"""
            **{f['pdf']}**  
            <div class='response-box'>{f['texto']}</div>
            """, unsafe_allow_html=True)
