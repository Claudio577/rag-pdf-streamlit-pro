from src.llm import get_llm
from langchain_core.messages import HumanMessage

def process_query(query, vectorstore):
    """Executa RAG completo: busca + geração."""

    retriever = vectorstore.as_retriever(search_kwargs={"k": 8})
    docs = retriever.get_relevant_documents(query)

    contexto = ""
    fontes = []

    for d in docs:
        texto = d.page_content.replace("passage: ", "")
        pdf = d.metadata.get("pdf_name")

        contexto += f"\n\n[PDF: {pdf}]\n{texto}"
        fontes.append({"pdf": pdf, "texto": texto})

    prompt = f"""
Você é um modelo RAG. Responda APENAS com informações dos PDFs abaixo.
Se a resposta não estiver no contexto, diga: 
"Não encontrei essa informação nos PDFs enviados."

### CONTEXTO:
{contexto}

### PERGUNTA:
{query}

### RESPOSTA:
"""

    resposta = get_llm().invoke([HumanMessage(content=prompt)])

    return resposta.content, fontes
