import os
import logging
import time
from typing import List, Dict, Any
import requests
from utils.retry import retry_with_backoff

logger = logging.getLogger(__name__)

# Colores para diferentes fuentes
COLORS = {
    "cdti": 0x1f77b4,      # Azul
    "red.es": 0xff7f0e,    # Naranja  
    "accio": 0x2ca02c,     # Verde
    "default": 0x9467bd    # Púrpura
}

@retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(requests.RequestException,))
def send_discord_message(webhook_url: str, payload: Dict[str, Any]) -> bool:
    """Envía un mensaje individual a Discord con reintentos."""
    try:
        response = requests.post(
            webhook_url, 
            json=payload, 
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 204:
            return True
        elif response.status_code == 429:  # Rate limit
            retry_after = int(response.headers.get('Retry-After', 5))
            logger.warning(f"Rate limit alcanzado. Esperando {retry_after} segundos...")
            time.sleep(retry_after)
            raise requests.RequestException("Rate limit - reintentando")
        else:
            logger.error(f"Error Discord {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error enviando mensaje a Discord: {e}")
        raise

def validate_webhook_url(url: str) -> bool:
    """Valida que la URL del webhook sea correcta."""
    if not url:
        return False
    return url.startswith("https://discord.com/api/webhooks/") or url.startswith("https://discordapp.com/api/webhooks/")

def create_embed(convocatoria: Dict[str, Any]) -> Dict[str, Any]:
    """Crea un embed de Discord para una convocatoria."""
    fuente = convocatoria.get("fuente", "default")
    color = COLORS.get(fuente, COLORS["default"])
    
    embed = {
        "title": convocatoria.get("titulo", "Convocatoria sin título")[:256],  # Discord limit
        "description": convocatoria.get("resumen", "Sin descripción disponible")[:4096],  # Discord limit
        "url": convocatoria.get("url", ""),
        "color": color,
        "footer": {
            "text": f"Fuente: {fuente.upper()} • FundBot"
        },
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    }
    
    return embed

def send_to_discord(convocatorias: List[Dict[str, Any]]) -> bool:
    """
    Envía convocatorias a Discord mediante webhook.
    
    Args:
        convocatorias: Lista de convocatorias a enviar
    
    Returns:
        True si todas las notificaciones se enviaron correctamente
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    if not validate_webhook_url(webhook_url):
        logger.error("DISCORD_WEBHOOK_URL no configurada o inválida")
        return False
    
    if not convocatorias:
        logger.info("No hay convocatorias para enviar a Discord")
        return True
    
    logger.info(f"Enviando {len(convocatorias)} convocatorias a Discord...")
    
    success_count = 0
    for i, convocatoria in enumerate(convocatorias, 1):
        try:
            embed = create_embed(convocatoria)
            payload = {"embeds": [embed]}
            
            if send_discord_message(webhook_url, payload):
                success_count += 1
                logger.debug(f"✅ {i}/{len(convocatorias)}: {convocatoria.get('titulo', 'Sin título')[:50]}...")
            else:
                logger.error(f"❌ {i}/{len(convocatorias)}: Falló envío de {convocatoria.get('titulo', 'Sin título')[:50]}...")
            
            # Pequeña pausa entre mensajes para evitar rate limiting
            if i < len(convocatorias):
                time.sleep(0.5)
                
        except Exception as e:
            logger.error(f"Error procesando convocatoria {i}: {e}")
            continue
    
    total = len(convocatorias)
    if success_count == total:
        logger.info(f"✅ Todas las notificaciones enviadas correctamente ({success_count}/{total})")
        return True
    else:
        logger.warning(f"⚠️ Notificaciones parciales: {success_count}/{total} enviadas correctamente")
        return False