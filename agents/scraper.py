import requests
from bs4 import BeautifulSoup

PORTALES = {
    "cdti": "https://www.cdti.es/es/convocatorias",
    "red.es": "https://www.red.es/es/buscador-de-ayudas",
    "accio": "https://www.accio.gencat.cat/ca/ajuts/"
}

def scrape_portals():
    result = []
    for key, url in PORTALES.items():
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                text = a.get_text(strip=True)
                if "convocatoria" in href.lower() or "ayuda" in text.lower():
                    full_url = href if href.startswith("http") else f"https://{key}.es{href}"
                    result.append({"fuente": key, "titulo": text, "url": full_url})
        except Exception as e:
            print(f"[WARN] Error scrapeando {key}: {e}")
    return result