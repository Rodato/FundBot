import sqlite3
import logging
from contextlib import contextmanager
from typing import List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

DB_FILE = "fundbot.db"

@contextmanager
def get_db_connection():
    """Context manager para conexiones de base de datos."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE, timeout=30.0)
        conn.row_factory = sqlite3.Row  # Para acceso por nombre de columna
        yield conn
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Error de base de datos: {e}")
        raise
    finally:
        if conn:
            conn.close()

def init_db() -> None:
    """Crea la tabla de la base de datos si no existe."""
    logger.info("Inicializando base de datos...")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS convocatorias (
            url TEXT PRIMARY KEY,
            titulo TEXT,
            fuente TEXT,
            fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        
        # Agregar índices para mejorar performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fuente ON convocatorias(fuente)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fecha ON convocatorias(fecha_agregado)")
        conn.commit()
        
        logger.info("Base de datos inicializada correctamente")

def url_exists(url: str) -> bool:
    """Comprueba si una URL ya existe en la base de datos."""
    if not url:
        return False
        
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM convocatorias WHERE url = ?", (url,))
            exists = cursor.fetchone() is not None
            
            if exists:
                logger.debug(f"URL ya existe en BD: {url[:50]}...")
            
            return exists
    except Exception as e:
        logger.error(f"Error verificando URL {url}: {e}")
        return False

def add_url(url: str, titulo: str = "", fuente: str = "") -> bool:
    """Añade una nueva URL a la base de datos."""
    if not url:
        logger.warning("Intento de agregar URL vacía")
        return False
        
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO convocatorias (url, titulo, fuente) VALUES (?, ?, ?)",
                (url, titulo, fuente)
            )
            
            if cursor.rowcount > 0:
                logger.info(f"Nueva URL agregada: {titulo} ({fuente})")
                conn.commit()
                return True
            else:
                logger.debug(f"URL ya existía: {url[:50]}...")
                return False
                
    except Exception as e:
        logger.error(f"Error agregando URL {url}: {e}")
        return False

def get_stats() -> dict:
    """Obtiene estadísticas de la base de datos."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Total de URLs
            cursor.execute("SELECT COUNT(*) as total FROM convocatorias")
            total = cursor.fetchone()["total"]
            
            # Por fuente
            cursor.execute("""
                SELECT fuente, COUNT(*) as count 
                FROM convocatorias 
                WHERE fuente != '' 
                GROUP BY fuente 
                ORDER BY count DESC
            """)
            por_fuente = dict(cursor.fetchall())
            
            # URLs agregadas hoy
            cursor.execute("""
                SELECT COUNT(*) as hoy 
                FROM convocatorias 
                WHERE DATE(fecha_agregado) = DATE('now')
            """)
            agregadas_hoy = cursor.fetchone()["hoy"]
            
            return {
                "total": total,
                "por_fuente": por_fuente,
                "agregadas_hoy": agregadas_hoy
            }
            
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        return {"total": 0, "por_fuente": {}, "agregadas_hoy": 0}
