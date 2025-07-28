import os
import requests
import json

def send_to_discord(convocatorias):
    url = os.getenv("DISCORD_WEBHOOK_URL")
    if not url:
        print("⚠️ DISCORD_WEBHOOK_URL no definida")
        return
    for c in convocatorias:
        payload = {
            "embeds": [{
                "title": c["titulo"],
                "description": c["resumen"],
                "url": c["url"],
                "color": 0x00ff00
            }]
        }
        resp = requests.post(url, json=payload)
        if resp.status_code != 204:
            print("❌ Error Discord:", resp.text)