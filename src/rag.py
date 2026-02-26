from src.llm import get_llm
from langchain_core.messages import HumanMessage


# =========================================================
# Função principal de processamento RAG
# =========================================================
def process_query(query, vectorstore):

    # ---------------------------------------------------------
    # Comando especial: resumo completo
    # ---------------------------------------------------------
    is_resumo_completo = query == "RESUMO_COMPLETO_PDF"

    if is_resumo_completo:
        query = "Faça um resumo completo, detalhado, organizado e fiel ao conteúdo do PDF."

    # ---------------------------------------------------------
    # Validação do vectorstore
    # ---------------------------------------------------------
    if vectorstore is None:
        raise ValueError("Vectorstore está vazio. Nenhum PDF foi indexado.")

    # ---------------------------------------------------------
    # Retriever (limites seguros)
    # ---------------------------------------------------------
    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 6,
            "fetch_k": 20,
            "maximal_marginal_relevance": True
        }
    )

    # ---------------------------------------------------------
    # Busca dos documentos
    # ---------------------------------------------------------
    try:
        docs = retriever.invoke(query)
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar documentos no retriever: {e}")

    if not docs:
        return "Nenhuma resposta encontrada nos PDFs.", []

    # ---------------------------------------------------------
    # Montagem do contexto (com limite)
    # ---------------------------------------------------------
    contexto = ""
    fontes = []
    MAX_CHARS = 12000  # seguro para gpt-4o / gpt-4o-mini

    for d in docs:
        texto = d.page_content.replace("passage: ", "")
        pdf = d.metadata.get("pdf_name", "PDF desconhecido")

        bloco = f"\n\n[PDF: {pdf}]\n{texto}"

        if len(contexto) + len(bloco) > MAX_CHARS:
            break

        contexto += bloco
        fontes.append({"pdf": pdf, "texto": texto})

    # ---------------------------------------------------------
    # Prompt RAG profissional
    # ---------------------------------------------------------
    prompt = f"""
Você é um assistente RAG especializado em leitura de documentos oficiais, jurídicos e administrativos.

Use APENAS os trechos fornecidos no CONTEXTO para responder.
Você pode:
- Resumir e reorganizar informações
- Explicar com outras palavras
- Unificar informações de diferentes partes do PDF
- Destacar regras, obrigações, prazos, responsabilidades e objetivos

REGRAS IMPORTANTES:
- Nunca invente informações
- Não use conhecimento externo
- Só diga que algo não foi encontrado se realmente não existir no contexto

### CONTEXTO (trechos reais do PDF):
{contexto}

### PERGUNTA:
{query}

### RESPOSTA (clara, organizada e fiel aos trechos):
"""

    # ---------------------------------------------------------
    # Chamada segura ao LLM
    # ---------------------------------------------------------
    try:
        resposta = get_llm().invoke([HumanMessage(content=prompt)])
    except Exception as e:
        raise RuntimeError(f"Erro ao chamar o LLM: {e}")

    return resposta.content, fontes
