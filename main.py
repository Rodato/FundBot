#!/usr/bin/env python3
"""
FundBot - Bot automatizado para encontrar y notificar convocatorias de financiación
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging antes de importar módulos
from utils.logger import setup_logger, log_execution_metrics

# Configurar logger principal
log_level = os.getenv("LOG_LEVEL", "INFO")
log_file = os.getenv("LOG_FILE", "logs/fundbot.log")
logger = setup_logger("fundbot", log_level, log_file)

# Importar agents después del logging
from agents.scraper import scrape_portals
from agents.classifier import classify_convocatorias
from agents.summarizer import summarize_relevant
from agents.notifier import send_to_discord
from agents.database import init_db, url_exists, add_url, get_stats

def validate_environment() -> bool:
    """Valida que las variables de entorno requeridas estén configuradas."""
    required_vars = ["GOOGLE_API_KEY", "DISCORD_WEBHOOK_URL"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Variables de entorno faltantes: {', '.join(missing_vars)}")
        logger.error("Configura las variables en un archivo .env o como variables de sistema")
        return False
    
    logger.info("✅ Variables de entorno validadas correctamente")
    return True

def main():
    """Función principal del bot."""
    start_time = datetime.now()
    logger.info("🚀 Iniciando FundBot...")
    
    try:
        # 1. Validar configuración
        if not validate_environment():
            logger.error("Configuración inválida. Abortando ejecución.")
            sys.exit(1)
        
        # 2. Inicializar base de datos
        logger.info("Inicializando base de datos...")
        init_db()
        
        # Mostrar estadísticas iniciales
        stats = get_stats()
        logger.info(f"Estadísticas BD: {stats['total']} URLs total, {stats['agregadas_hoy']} agregadas hoy")
        
        # 3. Scraping de portales
        logger.info("=== FASE 1: SCRAPING ===")
        raw_convocatorias = scrape_portals()
        
        if not raw_convocatorias:
            logger.warning("No se encontraron convocatorias en ningún portal")
            return
        
        # 4. Clasificación de relevancia
        logger.info("=== FASE 2: CLASIFICACIÓN ===")
        relevant_convocatorias = classify_convocatorias(raw_convocatorias)
        
        if not relevant_convocatorias:
            logger.info("No se encontraron convocatorias relevantes")
            log_execution_metrics(logger, start_time, len(os.getenv("portales", [])), 
                                len(raw_convocatorias), 0, 0)
            return
        
        # 5. Filtrar convocatorias nuevas
        logger.info("=== FASE 3: FILTRADO DE DUPLICADOS ===")
        nuevas_convocatorias = []
        for conv in relevant_convocatorias:
            if not url_exists(conv["url"]):
                nuevas_convocatorias.append(conv)
            else:
                logger.debug(f"Convocatoria ya existe: {conv['titulo'][:50]}...")
        
        logger.info(f"Filtrado completado: {len(nuevas_convocatorias)} nuevas de {len(relevant_convocatorias)} relevantes")
        
        if not nuevas_convocatorias:
            logger.info("✅ No hay nuevas convocatorias para procesar")
            log_execution_metrics(logger, start_time, len(os.getenv("portales", [])), 
                                len(raw_convocatorias), len(relevant_convocatorias), 0)
            return
        
        # 6. Generar resúmenes
        logger.info("=== FASE 4: GENERACIÓN DE RESÚMENES ===")
        convocatorias_resumidas = summarize_relevant(nuevas_convocatorias)
        
        # 7. Enviar notificaciones
        logger.info("=== FASE 5: NOTIFICACIONES ===")
        notification_success = send_to_discord(convocatorias_resumidas)
        
        # 8. Guardar en base de datos
        logger.info("=== FASE 6: PERSISTENCIA ===")
        saved_count = 0
        for conv in convocatorias_resumidas:
            if add_url(conv["url"], conv.get("titulo", ""), conv.get("fuente", "")):
                saved_count += 1
        
        logger.info(f"Guardadas {saved_count} nuevas URLs en base de datos")
        
        # 9. Métricas finales
        log_execution_metrics(
            logger, start_time, 
            len(os.getenv("portales", [])), 
            len(raw_convocatorias),
            len(relevant_convocatorias), 
            len(convocatorias_resumidas)
        )
        
        if notification_success:
            logger.info(f"🎉 Ejecución completada exitosamente: {len(convocatorias_resumidas)} nuevas convocatorias procesadas")
        else:
            logger.warning("⚠️ Ejecución completada con errores en las notificaciones")
        
    except KeyboardInterrupt:
        logger.info("Ejecución interrumpida por el usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error crítico durante la ejecución: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
