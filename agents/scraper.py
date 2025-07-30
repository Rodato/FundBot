import os
import json
import logging
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from urllib.parse import urljoin
from utils.retry import robust_http_request, retry_with_backoff

logger = logging.getLogger(__name__)

# Inicializamos el modelo LLM una sola vez
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def load_portals_config() -> Dict[str, str]:
    """Carga la configuración de portales desde portales.json."""
    try:
        with open("portales.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            logger.info(f"Configuración cargada: {len(config)} portales")
            return config
    except FileNotFoundError:
        logger.error("portales.json no encontrado. Asegúrate de que existe en la raíz del proyecto.")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"portales.json no es un JSON válido: {e}")
        return {}

PORTALES = load_portals_config()

@retry_with_backoff(max_retries=2, base_delay=1.0, exceptions=(Exception,))
def extract_convocatorias_with_llm(html_content: str, base_url: str) -> List[Dict[str, Any]]:
    """
    Usa un LLM para extraer convocatorias de un contenido HTML.
    """
    logger.debug(f"Extrayendo convocatorias con LLM para: {base_url}")
    
    # Limitar el contenido HTML para evitar tokens excesivos
    max_html_length = 15000
    truncated_html = html_content[:max_html_length]
    if len(html_content) > max_html_length:
        logger.warning(f"HTML truncado de {len(html_content)} a {max_html_length} caracteres")
    
    prompt = f"""
    Eres un asistente experto en web scraping. Analiza el siguiente contenido HTML y extrae todas las convocatorias, ayudas o subvenciones que encuentres.

    Para cada convocatoria, extrae:
    1.  `titulo`: El nombre o título principal de la convocatoria.
    2.  `url`: La URL completa y absoluta que lleva al detalle de la convocatoria.
    3.  `resumen`: Una breve descripción o el texto que la acompaña, si está disponible.

    Devuelve el resultado como un array de objetos JSON válido. Asegúrate de que las URLs sean absolutas. La URL base de la página es: {base_url}

    Si no encuentras ninguna convocatoria, devuelve un array JSON vacío: [].

    HTML:
    ```html
    {truncated_html}
    ```
    """
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        clean_response = response.content.strip()
        
        # Limpiar respuesta del LLM
        if clean_response.startswith("```json"):
            clean_response = clean_response[7:]
        if clean_response.endswith("```"):
            clean_response = clean_response[:-3]
        clean_response = clean_response.strip()

        convocatorias = json.loads(clean_response)
        
        if not isinstance(convocatorias, list):
            logger.warning(f"LLM no devolvió una lista para {base_url}")
            return []

        # Validar y normalizar URLs
        valid_convocatorias = []
        for c in convocatorias:
            if not isinstance(c, dict) or 'titulo' not in c or 'url' not in c:
                logger.warning(f"Convocatoria inválida ignorada: {c}")
                continue
                
            c["url"] = urljoin(base_url, c["url"])
            if not c.get("resumen"):
                c["resumen"] = ""
            
            valid_convocatorias.append(c)

        logger.debug(f"Extraídas {len(valid_convocatorias)} convocatorias válidas")
        return valid_convocatorias
        
    except json.JSONDecodeError as e:
        logger.error(f"Error decodificando JSON de LLM para {base_url}: {e}")
        logger.debug(f"Respuesta problemática: {clean_response[:200]}...")
        return []
    except Exception as e:
        logger.error(f"Error procesando respuesta del LLM para {base_url}: {e}")
        return []

def scrape_portals() -> List[Dict[str, Any]]:
    """
    Recorre la lista de portales, obtiene su HTML y usa el LLM para extraer la información.
    """
    if not PORTALES:
        logger.error("No hay portales configurados para scrapear")
        return []
    
    result = []
    total_portales = len(PORTALES)
    
    logger.info(f"Iniciando scraping de {total_portales} portales")
    
    for key, url in PORTALES.items():
        logger.info(f"Scrapeando {key} ({url})")
        
        try:
            # Usar función robusta con reintentos
            response = robust_http_request(url)
            
            if not response.text.strip():
                logger.warning(f"Respuesta vacía de {key}")
                continue
            
            convocatorias = extract_convocatorias_with_llm(response.text, url)
            
            # Agregar fuente a cada convocatoria
            for c in convocatorias:
                c["fuente"] = key
                result.append(c)
            
            logger.info(f"✅ {key}: {len(convocatorias)} convocatorias encontradas")

        except Exception as e:
            logger.error(f"Error scrapeando {key}: {e}")
            continue

    logger.info(f"Scraping completado: {len(result)} convocatorias totales de {total_portales} portales")
    return result

