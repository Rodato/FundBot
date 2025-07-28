from dotenv import load_dotenv
load_dotenv()

import os
from datetime import datetime
from agents.scraper import scrape_portals
from agents.classifier import classify_convocatorias
from agents.summarizer import summarize_relevant
from agents.notifier import send_to_discord

if __name__ == "__main__":
    raw = scrape_portals()
    relevant = classify_convocatorias(raw)
    summary = summarize_relevant(relevant)

    os.makedirs("data", exist_ok=True)
    filename = f"data/convocatorias_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(f"{s}\n" for s in summary)

    send_to_discord(summary)
    print(f"✅ Proceso terminado. Resumen enviado a Discord y guardado en {filename}")