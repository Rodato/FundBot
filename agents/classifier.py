import os
import logging
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from utils.retry import retry_with_backoff

logger = logging.getLogger(__name__)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", 
    temperature=0, 
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

COMPANY_PROFILE = """
Empresa COLOMBIANA especializada en CIENCIA DE DATOS, VISUALIZACIÓN DE DATOS e INTELIGENCIA ARTIFICIAL:

UBICACIÓN: COLOMBIA (empresa latinoamericana)

ÁREAS PRINCIPALES:
- Ciencia de datos y análisis avanzado
- Visualización de datos y dashboards interactivos
- Inteligencia Artificial y Machine Learning
- Business Intelligence y analítica empresarial
- Big Data y procesamiento de datos masivos
- Modelos predictivos y algoritmos de IA

TECNOLOGÍAS:
- Python, R, SQL para análisis de datos
- Frameworks de ML: TensorFlow, PyTorch, Scikit-learn
- Herramientas de visualización: Tableau, Power BI, D3.js
- Plataformas cloud: AWS, Azure, Google Cloud
- Bases de datos: SQL, NoSQL, Data Lakes

SECTORES DE APLICACIÓN:
- Transformación digital empresarial
- Automatización con IA
- Análisis predictivo para empresas
- Soluciones de Business Intelligence
- Consultoría en ciencia de datos

ELEGIBILIDAD REQUERIDA:
- Convocatorias abiertas para empresas COLOMBIANAS
- Programas internacionales que incluyan Latinoamérica
- Fondos que permitan participación desde Colombia
- NO convocatorias exclusivas de España o UE sin participación internacional
"""

@retry_with_backoff(max_retries=2, base_delay=0.5, exceptions=(Exception,))
def classify_single_convocatoria(convocatoria: Dict[str, Any]) -> bool:
    """Clasifica una sola convocatoria usando el LLM."""
    try:
        prompt = f"""
Analiza esta convocatoria y responde ÚNICAMENTE "SI" o "NO":

{COMPANY_PROFILE}

Convocatoria:
- Título: {convocatoria.get('titulo', 'Sin título')}
- Resumen: {convocatoria.get('resumen', 'Sin resumen')[:200]}
- URL: {convocatoria.get('url', '')}

¿Esta convocatoria es relevante para nuestra empresa? Responde solo SI o NO.
"""
        
        response = llm.invoke([HumanMessage(content=prompt)])
        resultado = response.content.strip().upper()
        
        # Validar respuesta
        if resultado not in ["SI", "NO"]:
            logger.warning(f"Respuesta inesperada del LLM: '{resultado}'. Asumiendo NO.")
            return False
            
        is_relevant = resultado == "SI"
        
        if is_relevant:
            logger.debug(f"✅ Relevante: {convocatoria.get('titulo', 'Sin título')[:50]}...")
        else:
            logger.debug(f"❌ No relevante: {convocatoria.get('titulo', 'Sin título')[:50]}...")
            
        return is_relevant
        
    except Exception as e:
        logger.error(f"Error clasificando convocatoria {convocatoria.get('titulo', 'Sin título')}: {e}")
        return False

def classify_convocatorias(convocatorias: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Clasifica una lista de convocatorias para determinar relevancia.
    
    Args:
        convocatorias: Lista de convocatorias a clasificar
    
    Returns:
        Lista de convocatorias relevantes
    """
    if not convocatorias:
        logger.info("No hay convocatorias para clasificar")
        return []
    
    logger.info(f"Clasificando {len(convocatorias)} convocatorias...")
    
    aprobadas = []
    for i, convocatoria in enumerate(convocatorias, 1):
        logger.debug(f"Clasificando {i}/{len(convocatorias)}: {convocatoria.get('titulo', 'Sin título')[:50]}...")
        
        if classify_single_convocatoria(convocatoria):
            aprobadas.append(convocatoria)
    
    logger.info(f"Clasificación completa: {len(aprobadas)}/{len(convocatorias)} convocatorias relevantes")
    return aprobadas