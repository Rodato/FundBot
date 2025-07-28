import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("DISCORD_WEBHOOK_URL")
if not url:
    print("⚠️ DISCORD_WEBHOOK_URL no definida")
else:
    payload = {
        "content": "Hola, esto es una prueba desde FundBot."
    }
    resp = requests.post(url, json=payload)
    if resp.status_code == 204:
        print("✅ Mensaje de prueba enviado a Discord.")
    else:
        print(f"❌ Error Discord: {resp.status_code}")
        print(resp.text)
