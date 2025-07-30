#!/usr/bin/env python3
"""
Pruebas básicas que no requieren APIs externas
"""

import os
import sys
import tempfile
from datetime import datetime

# Configurar logging
from utils.logger import setup_logger

logger = setup_logger("fundbot-basic-test", "DEBUG")

def test_imports():
    """Prueba que todos los módulos se pueden importar correctamente."""
    logger.info("=== PRUEBA 1: IMPORTS ===")
    
    try:
        from agents.database import init_db, add_url, url_exists, get_stats
        logger.info("✅ Módulo database importado")
        
        from agents.scraper import load_portals_config
        logger.info("✅ Módulo scraper importado")
        
        from agents.notifier import validate_webhook_url, create_embed
        logger.info("✅ Módulo notifier importado")
        
        from utils.logger import setup_logger, log_execution_metrics
        logger.info("✅ Módulo logger importado")
        
        from utils.retry import retry_with_backoff, robust_http_request
        logger.info("✅ Módulo retry importado")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error importando módulos: {e}")
        return False

def test_database_operations():
    """Prueba las operaciones básicas de base de datos."""
    logger.info("=== PRUEBA 2: BASE DE DATOS ===")
    
    try:
        from agents.database import init_db, add_url, url_exists, get_stats
        
        # Usar base de datos temporal
        test_db = f"test_fundbot_{datetime.now().timestamp()}.db"
        original_db_file = None
        
        # Cambiar temporalmente la configuración de BD
        import agents.database
        original_db_file = agents.database.DB_FILE
        agents.database.DB_FILE = test_db
        
        # Probar inicialización
        init_db()
        logger.info("✅ Base de datos inicializada")
        
        # Probar inserción
        test_url = f"https://test.example.com/{datetime.now().timestamp()}"
        result = add_url(test_url, "Prueba de convocatoria", "test")
        logger.info(f"✅ URL agregada: {result}")
        
        # Probar verificación de existencia
        exists = url_exists(test_url)
        if exists:
            logger.info("✅ URL existe en BD")
        else:
            logger.error("❌ URL no encontrada en BD")
            return False
        
        # Probar URL no existente
        non_existent = url_exists("https://no-existe.com")
        if not non_existent:
            logger.info("✅ URL inexistente correctamente identificada")
        else:
            logger.error("❌ URL inexistente mal identificada")
            return False
        
        # Probar estadísticas
        stats = get_stats()
        logger.info(f"✅ Estadísticas obtenidas: {stats}")
        
        if stats["total"] >= 1:
            logger.info("✅ Conteo de estadísticas correcto")
        else:
            logger.error("❌ Conteo de estadísticas incorrecto")
            return False
        
        # Limpiar
        if os.path.exists(test_db):
            os.remove(test_db)
        
        # Restaurar configuración
        if original_db_file:
            agents.database.DB_FILE = original_db_file
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de BD: {e}")
        return False

def test_config_loading():
    """Prueba la carga de configuración."""
    logger.info("=== PRUEBA 3: CONFIGURACIÓN ===")
    
    try:
        from agents.scraper import load_portals_config
        
        # Probar con archivo existente
        if os.path.exists("portales.json"):
            config = load_portals_config()
            logger.info(f"✅ Configuración cargada: {len(config)} portales")
            
            # Validar que sea un diccionario
            if isinstance(config, dict):
                logger.info("✅ Formato de configuración correcto")
            else:
                logger.error("❌ Formato de configuración incorrecto")
                return False
                
            # Validar que las URLs sean válidas
            for name, url in config.items():
                if url.startswith(("http://", "https://")):
                    logger.info(f"✅ URL válida para {name}: {url}")
                else:
                    logger.warning(f"⚠️ URL posiblemente inválida para {name}: {url}")
        else:
            logger.warning("⚠️ portales.json no encontrado")
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de configuración: {e}")
        return False

def test_webhook_validation():
    """Prueba la validación de webhooks de Discord."""
    logger.info("=== PRUEBA 4: VALIDACIÓN WEBHOOK ===")
    
    try:
        from agents.notifier import validate_webhook_url, create_embed
        
        # Probar URLs válidas
        valid_urls = [
            "https://discord.com/api/webhooks/123456789/abcdefghijklmnop",
            "https://discordapp.com/api/webhooks/987654321/zyxwvutsrqponmlk"
        ]
        
        for url in valid_urls:
            if validate_webhook_url(url):
                logger.info(f"✅ URL válida: {url[:50]}...")
            else:
                logger.error(f"❌ URL válida rechazada: {url[:50]}...")
                return False
        
        # Probar URLs inválidas
        invalid_urls = [
            "",
            "https://google.com",
            "not-a-url",
            "https://discord.com/invalid"
        ]
        
        for url in invalid_urls:
            if not validate_webhook_url(url):
                logger.info(f"✅ URL inválida rechazada: {url}")
            else:
                logger.error(f"❌ URL inválida aceptada: {url}")
                return False
        
        # Probar creación de embed
        test_convocatoria = {
            "titulo": "Convocatoria de prueba",
            "resumen": "Esta es una convocatoria de prueba para validar el embed",
            "url": "https://test.example.com/convocatoria",
            "fuente": "test"
        }
        
        embed = create_embed(test_convocatoria)
        
        # Validar estructura del embed
        required_fields = ["title", "description", "url", "color", "footer", "timestamp"]
        for field in required_fields:
            if field in embed:
                logger.info(f"✅ Campo {field} presente en embed")
            else:
                logger.error(f"❌ Campo {field} faltante en embed")
                return False
        
        # Validar límites de Discord
        if len(embed["title"]) <= 256:
            logger.info("✅ Título dentro del límite de Discord")
        else:
            logger.error("❌ Título excede límite de Discord")
            return False
            
        if len(embed["description"]) <= 4096:
            logger.info("✅ Descripción dentro del límite de Discord")
        else:
            logger.error("❌ Descripción excede límite de Discord")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de webhook: {e}")
        return False

def test_retry_decorator():
    """Prueba el decorador de reintentos."""
    logger.info("=== PRUEBA 5: DECORADOR DE REINTENTOS ===")
    
    try:
        from utils.retry import retry_with_backoff
        
        # Contador para simular fallos
        attempt_count = 0
        
        @retry_with_backoff(max_retries=2, base_delay=0.1, exceptions=(ValueError,))
        def failing_function():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise ValueError(f"Intento {attempt_count} falló")
            return f"Éxito en intento {attempt_count}"
        
        # Ejecutar función que falla y luego tiene éxito
        result = failing_function()
        
        if "Éxito" in result and attempt_count == 3:
            logger.info(f"✅ Reintentos funcionando: {result}")
        else:
            logger.error(f"❌ Reintentos no funcionando correctamente: {result}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de reintentos: {e}")
        return False

def main():
    """Ejecuta todas las pruebas básicas."""
    logger.info("🧪 Iniciando pruebas básicas del sistema FundBot...")
    
    tests = [
        ("Imports", test_imports),
        ("Base de datos", test_database_operations),
        ("Configuración", test_config_loading),
        ("Webhook validation", test_webhook_validation),
        ("Retry decorator", test_retry_decorator)
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
    logger.info("=== RESUMEN DE PRUEBAS BÁSICAS ===")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} {test_name}")
        if result:
            passed += 1
    
    logger.info(f"Resultado final: {passed}/{total} pruebas básicas exitosas")
    
    if passed == total:
        logger.info("🎉 ¡Todas las pruebas básicas pasaron!")
        return True
    else:
        logger.warning("⚠️ Algunas pruebas básicas fallaron.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)