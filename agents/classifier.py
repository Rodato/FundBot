from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def classify_convocatorias(convocatorias):
    aprobadas = []
    for c in convocatorias:
        prompt = f"""Analiza esta convocatoria y responde solo SI o NO:
Título: {c['titulo']}
URL: {c['url']}
¿Encaja con una empresa especializada en IA, visualización de datos y dashboards?"""
        if llm.invoke([HumanMessage(content=prompt)]).content.strip().upper() == "SI":
            aprobadas.append(c)
    return aprobadas