from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def summarize_relevant(convocatorias):
    resumidos = []
    for c in convocatorias:
        prompt = f"""Resume en ≤100 palabras:
- Nombre de la convocatoria
- Fecha límite (si aparece)
- Por qué encaja para una empresa de IA/visualización
- URL: {c['url']}

Título: {c['titulo']}"""
        resumen = llm.invoke([HumanMessage(content=prompt)]).content.strip()
        resumidos.append({"titulo": c["titulo"], "url": c["url"], "resumen": resumen})
    return resumidos