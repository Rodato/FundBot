from dotenv import load_dotenv
load_dotenv()

from agents.scraper import scrape_portals
from agents.classifier import classify_convocatorias
from agents.summarizer import summarize_relevant
from agents.notifier import send_to_discord
from agents.database import init_db, url_exists, add_url

if __name__ == "__main__":
    # 1. Inicializar la base de datos
    init_db()

    # 2. Obtener todas las convocatorias de los portales
    raw = scrape_portals()

    # 3. Clasificar para encontrar las relevantes
    relevant = classify_convocatorias(raw)

    # 4. Filtrar las que ya han sido notificadas
    nuevas = [c for c in relevant if not url_exists(c["url"])]

    if not nuevas:
        print("✅ No se encontraron nuevas convocatorias.")
    else:
        print(f"📢 Encontradas {len(nuevas)} nuevas convocatorias.")
        # 5. Resumir solo las nuevas
        summary = summarize_relevant(nuevas)

        # 6. Enviar a Discord
        send_to_discord(summary)

        # 7. Guardar las nuevas en la base de datos para no repetirlas
        for c in summary:
            add_url(c["url"])
        
        print(f"✅ Proceso terminado. {len(summary)} nuevas convocatorias enviadas y guardadas.")
