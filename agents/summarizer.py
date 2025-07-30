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

@retry_with_backoff(max_retries=2, base_delay=0.5, exceptions=(Exception,))
def summarize_single_convocatoria(convocatoria: Dict[str, Any]) -> str:
    """Genera un resumen para una sola convocatoria."""
    try:
        titulo = convocatoria.get('titulo', 'Convocatoria sin título')
        url = convocatoria.get('url', '')
        resumen_original = convocatoria.get('resumen', '')
        fuente = convocatoria.get('fuente', 'Fuente desconocida')
        
        prompt = f"""
Crea un resumen ejecutivo en español de máximo 100 palabras que incluya:

1. Nombre de la convocatoria
2. Fecha límite (si se menciona)
3. Por qué es relevante para una empresa de IA/visualización/dashboards
4. Aspectos clave o requisitos importantes

Información disponible:
- Título: {titulo}
- Descripción: {resumen_original[:300]}
- Fuente: {fuente}
- URL: {url}

Formato: Párrafo conciso y profesional.
"""
        
        response = llm.invoke([HumanMessage(content=prompt)])
        resumen = response.content.strip()
        
        if not resumen:
            logger.warning(f"Resumen vacío para: {titulo[:50]}...")
            return f"Convocatoria relevante para empresas de IA y visualización de datos. Ver detalles en: {url}"
        
        logger.debug(f"Resumen generado para: {titulo[:50]}...")
        return resumen
        
    except Exception as e:
        logger.error(f"Error generando resumen para {convocatoria.get('titulo', 'Sin título')}: {e}")
        return f"Error generando resumen. Ver detalles en: {convocatoria.get('url', '')}"

def summarize_relevant(convocatorias: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Genera resúmenes para una lista de convocatorias relevantes.
    
    Args:
        convocatorias: Lista de convocatorias a resumir
    
    Returns:
        Lista de convocatorias con resúmenes generados
    """
    if not convocatorias:
        logger.info("No hay convocatorias para resumir")
        return []
    
    logger.info(f"Generando resúmenes para {len(convocatorias)} convocatorias...")
    
    resumidos = []
    for i, convocatoria in enumerate(convocatorias, 1):
        logger.debug(f"Resumiendo {i}/{len(convocatorias)}: {convocatoria.get('titulo', 'Sin título')[:50]}...")
        
        resumen = summarize_single_convocatoria(convocatoria)
        
        resumidos.append({
            "titulo": convocatoria.get("titulo", "Sin título"),
            "url": convocatoria.get("url", ""),
            "resumen": resumen,
            "fuente": convocatoria.get("fuente", "")
        })
    
    logger.info(f"Resúmenes completados: {len(resumidos)} convocatorias procesadas")
    return resumidos