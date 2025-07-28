import os
import requests
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from urllib.parse import urljoin

# Inicializamos el modelo LLM una sola vez
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def load_portals_config():
    """Carga la configuración de portales desde portales.json."""
    try:
        with open("portales.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Error: portales.json no encontrado. Asegúrate de que existe en la raíz del proyecto.")
        return {}
    except json.JSONDecodeError:
        print("❌ Error: portales.json no es un JSON válido.")
        return {}

PORTALES = load_portals_config()

def extract_convocatorias_with_llm(html_content, base_url):
    """
    Usa un LLM para extraer convocatorias de un contenido HTML.
    """
    prompt = f"""
    Eres un asistente experto en web scraping. Analiza el siguiente contenido HTML y extrae todas las convocatorias, ayudas o subvenciones que encuentres.

    Para cada convocatoria, extrae:
    1.  `titulo`: El nombre o título principal de la convocatoria.
    2.  `url`: La URL completa y absoluta que lleva al detalle de la convocatoria.
    3.  `resumen`: Una breve descripción o el texto que la acompaña, si está disponible.

    Devuelve el resultado como un array de objetos JSON. Asegúrate de que las URLs sean absolutas. La URL base de la página es: {base_url}

    Si no encuentras ninguna convocatoria, devuelve un array JSON vacío: [].

    HTML:
    ```html
    {html_content[:10000]}
    ```
    """
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        # Limpiamos la respuesta para asegurarnos de que es un JSON válido
        clean_response = response.content.strip()
        if clean_response.startswith("```json"):
            clean_response = clean_response[7:-4].strip()

        convocatorias = json.loads(clean_response)

        # Nos aseguramos de que las URLs son absolutas
        for c in convocatorias:
            c["url"] = urljoin(base_url, c["url"])

        return convocatorias
    except (json.JSONDecodeError, Exception) as e:
        print(f"[ERROR] No se pudo procesar la respuesta del LLM para {base_url}: {e}")
        return []

def scrape_portals():
    """
    Recorre la lista de portales, obtiene su HTML y usa el LLM para extraer la información.
    """
    result = []
    for key, url in PORTALES.items():
        print(f"🔎 Scrapeando {key}...")
        try:
            res = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
            res.raise_for_status() # Lanza un error si la petición no fue exitosa

            convocatorias = extract_convocatorias_with_llm(res.text, url)
            for c in convocatorias:
                c["fuente"] = key
                result.append(c)
            print(f"✅ Encontradas {len(convocatorias)} convocatorias en {key}.")

        except requests.RequestException as e:
            print(f"[WARN] Error en la petición a {key}: {e}")
        except Exception as e:
            print(f"[WARN] Error inesperado scrapeando {key}: {e}")

    return result

