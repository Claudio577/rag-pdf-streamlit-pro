from src.llm import get_llm
from langchain_core.messages import HumanMessage

def process_query(query, vectorstore):

    if vectorstore is None:
        raise ValueError("Vectorstore está vazio. Nenhum PDF foi indexado.")

    retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 15,
        "fetch_k": 50,
        "maximal_marginal_relevance": True
    }
)


    # Usa o método correto do LangChain moderno
    try:
        docs = retriever.invoke(query)
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar documentos no retriever: {str(e)}")

    if not docs:
        return "Nenhuma resposta encontrada nos PDFs.", []

    contexto = ""
    fontes = []

    for d in docs:
        texto = d.page_content.replace("passage: ", "")
        pdf = d.metadata.get("pdf_name", "PDF desconhecido")

        contexto += f"\n\n[PDF: {pdf}]\n{texto}"
        fontes.append({"pdf": pdf, "texto": texto})

    # -------------------------------
    # PROMPT CORRIGIDO — ESSENCIAL
    # -------------------------------
    prompt = f"""
Você é um assistente RAG. Use APENAS o conteúdo dos PDFs abaixo
para responder à pergunta do usuário.

Você pode:
- Resumir o conteúdo
- Reescrever com outras palavras
- Explicar do que o PDF trata
- Extrair ideias principais
- Sintetizar informações do texto

NÃO diga "Não encontrei essa informação" se o PDF contiver qualquer fato relacionado.

Apenas diga isso caso REALMENTE não exista nada no contexto que ajude.

### CONTEXTO (trechos dos PDFs):
{contexto}

### PERGUNTA:
{query}

### RESPOSTA:
"""
    # -------------------------------

    resposta = get_llm().invoke([HumanMessage(content=prompt)])
    return resposta.content, fontes
