import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=os.getenv("GOOGLE_API_KEY"))

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