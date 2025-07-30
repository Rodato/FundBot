#!/usr/bin/env python3
"""
Script de prueba para validar el funcionamiento de FundBot sin enviar notificaciones reales.
"""

import os
import sys
import tempfile
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
from utils.logger import setup_logger

logger = setup_logger("fundbot-test", "DEBUG")

def test_environment():
    """Prueba las variables de entorno."""
    logger.info("=== PRUEBA 1: VARIABLES DE ENTORNO ===")
    
    required_vars = ["GOOGLE_API_KEY", "DISCORD_WEBHOOK_URL"]
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"✅ {var}: configurada (longitud: {len(value)})")
        else:
            logger.error(f"❌ {var}: NO configurada")
            all_good = False
    
    return all_good

def test_database():
    """Prueba la funcionalidad de base de datos."""
    logger.info("=== PRUEBA 2: BASE DE DATOS ===")
    
    try:
        from agents.database import init_db, add_url, url_exists, get_stats
        
        # Usar base de datos temporal para pruebas
        test_db = "test_fundbot.db"
        original_db = os.environ.get("DB_FILE", "fundbot.db")
        
        # Cambiar temporalmente la BD
        import agents.database
        agents.database.DB_FILE = test_db
        
        # Probar inicialización
        init_db()
        logger.info("✅ Base de datos inicializada")
        
        # Probar inserción
        test_url = f"https://test.example.com/{datetime.now().timestamp()}"
        result = add_url(test_url, "Prueba de convocatoria", "test")
        logger.info(f"✅ URL agregada: {result}")
        
        # Probar verificación
        exists = url_exists(test_url)
        logger.info(f"✅ URL existe: {exists}")
        
        # Probar estadísticas
        stats = get_stats()
        logger.info(f"✅ Estadísticas: {stats}")
        
        # Limpiar
        if os.path.exists(test_db):
            os.remove(test_db)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de BD: {e}")
        return False

def test_scraping():
    """Prueba el scraping de un portal."""
    logger.info("=== PRUEBA 3: SCRAPING ===")
    
    try:
        from agents.scraper import extract_convocatorias_with_llm
        
        # HTML de prueba
        test_html = """
        <html>
        <body>
            <div class="convocatoria">
                <h2><a href="/convocatoria1">Ayudas para innovación tecnológica 2024</a></h2>
                <p>Subvenciones para empresas tecnológicas que desarrollen soluciones de IA</p>
            </div>
            <div class="convocatoria">
                <h2><a href="/convocatoria2">Programa de digitalización empresarial</a></h2>
                <p>Apoyo para la transformación digital de PYMES</p>
            </div>
        </body>
        </html>
        """
        
        base_url = "https://test.example.com"
        convocatorias = extract_convocatorias_with_llm(test_html, base_url)
        
        logger.info(f"✅ Scraping completado: {len(convocatorias)} convocatorias extraídas")
        
        for i, conv in enumerate(convocatorias, 1):
            logger.info(f"  {i}. {conv.get('titulo', 'Sin título')}")
        
        return len(convocatorias) > 0
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de scraping: {e}")
        return False

def test_classification():
    """Prueba la clasificación de convocatorias."""
    logger.info("=== PRUEBA 4: CLASIFICACIÓN ===")
    
    try:
        from agents.classifier import classify_convocatorias
        
        # Convocatorias de prueba
        test_convocatorias = [
            {
                "titulo": "Ayudas para desarrollo de IA y Machine Learning",
                "url": "https://test.com/ia",
                "resumen": "Subvenciones para empresas que desarrollen soluciones de inteligencia artificial"
            },
            {
                "titulo": "Subvenciones para agricultura tradicional",
                "url": "https://test.com/agro",
                "resumen": "Ayudas para técnicas agrícolas tradicionales"
            },
            {
                "titulo": "Programa de visualización de datos empresariales",
                "url": "https://test.com/dataviz",
                "resumen": "Apoyo para desarrollar dashboards y herramientas de Business Intelligence"
            }
        ]
        
        relevant = classify_convocatorias(test_convocatorias)
        
        logger.info(f"✅ Clasificación completada: {len(relevant)}/{len(test_convocatorias)} relevantes")
        
        for conv in relevant:
            logger.info(f"  ✅ Relevante: {conv['titulo']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de clasificación: {e}")
        return False

def test_summarization():
    """Prueba la generación de resúmenes."""
    logger.info("=== PRUEBA 5: GENERACIÓN DE RESÚMENES ===")
    
    try:
        from agents.summarizer import summarize_relevant
        
        test_convocatorias = [
            {
                "titulo": "Ayudas CDTI para I+D en IA",
                "url": "https://test.com/cdti-ia",
                "resumen": "El CDTI ofrece subvenciones para proyectos de investigación en inteligencia artificial",
                "fuente": "cdti"
            }
        ]
        
        summaries = summarize_relevant(test_convocatorias)
        
        logger.info(f"✅ Resúmenes generados: {len(summaries)}")
        
        for summary in summaries:
            logger.info(f"  📝 {summary['titulo']}")
            logger.info(f"     {summary['resumen'][:100]}...")
        
        return len(summaries) > 0
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de resúmenes: {e}")
        return False

def test_discord_validation():
    """Prueba la validación de Discord sin enviar mensajes."""
    logger.info("=== PRUEBA 6: VALIDACIÓN DISCORD ===")
    
    try:
        from agents.notifier import validate_webhook_url, create_embed
        
        webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        
        if validate_webhook_url(webhook_url):
            logger.info("✅ URL de webhook válida")
        else:
            logger.error("❌ URL de webhook inválida")
            return False
        
        # Probar creación de embed
        test_conv = {
            "titulo": "Convocatoria de prueba",
            "resumen": "Esta es una convocatoria de prueba para validar el sistema",
            "url": "https://test.com/prueba",
            "fuente": "test"
        }
        
        embed = create_embed(test_conv)
        logger.info("✅ Embed creado correctamente")
        logger.info(f"  - Título: {embed['title']}")
        logger.info(f"  - Color: {hex(embed['color'])}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de Discord: {e}")
        return False

def main():
    """Ejecuta todas las pruebas."""
    logger.info("🧪 Iniciando pruebas del sistema FundBot...")
    
    tests = [
        ("Variables de entorno", test_environment),
        ("Base de datos", test_database),
        ("Scraping", test_scraping),
        ("Clasificación", test_classification),
        ("Resúmenes", test_summarization),
        ("Discord", test_discord_validation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Error ejecutando {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen final
    logger.info("=== RESUMEN DE PRUEBAS ===")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} {test_name}")
        if result:
            passed += 1
    
    logger.info(f"Resultado final: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        logger.info("🎉 ¡Todas las pruebas pasaron! El sistema está listo.")
        return True
    else:
        logger.warning("⚠️ Algunas pruebas fallaron. Revisa la configuración.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)