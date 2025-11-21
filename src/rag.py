from src.llm import get_llm
from langchain_core.messages import HumanMessage

def process_query(query, vectorstore):

    if vectorstore is None:
        raise ValueError("Vectorstore está vazio. Nenhum PDF foi indexado.")

    retriever = vectorstore.as_retriever(search_kwargs={"k": 8})

    # CORREÇÃO AQUI
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

    prompt = f"""
Responda APENAS com base nos PDFs abaixo.
Se não houver resposta, diga:
"Não encontrei essa informação nos PDFs enviados."

### CONTEXTO:
{contexto}

### PERGUNTA:
{query}

### RESPOSTA:
"""

    resposta = get_llm().invoke([HumanMessage(content=prompt)])
    return resposta.content, fontes
