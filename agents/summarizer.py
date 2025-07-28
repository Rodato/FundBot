import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=os.getenv("GOOGLE_API_KEY"))

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