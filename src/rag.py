from src.llm import get_llm
from langchain_core.messages import HumanMessage

def process_query(query, vectorstore):
# Detecta comando de resumo completo
if query == "RESUMO_COMPLETO_PDF":
    query = "Faça um resumo completo, detalhado, organizado e fiel ao PDF inteiro."

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

    # PROMPT PROFISSIONAL
    prompt = f"""
Você é um assistente RAG especializado em leitura de documentos oficiais, jurídicos e administrativos.

Use APENAS os trechos fornecidos no CONTEXTO para responder.  
No entanto, você pode:

- Resumir o conteúdo
- Explicar com outras palavras
- Inferir o tema geral a partir dos trechos
- Unificar informações de diferentes partes do PDF
- Estruturar a resposta de forma clara e organizada
- Destacar objetivos, regras, obrigações, prazos e responsabilidades

IMPORTANTE:
❗ Não responda "não encontrei" se houver QUALQUER trecho relacionado ao tema.  
❗ Só diga "não encontrei essa informação nos PDFs" se realmente não existir nada útil no contexto.  
❗ Nunca invente informações fora dos trechos fornecidos.

### CONTEXTO (trechos reais do PDF):
{contexto}

### PERGUNTA DO USUÁRIO:
{query}

### SUA RESPOSTA (clara, completa e baseada nos trechos acima):
"""

    resposta = get_llm().invoke([HumanMessage(content=prompt)])
    return resposta.content, fontes
