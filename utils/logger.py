import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

def setup_logger(name: str = "fundbot", level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Configura un logger estructurado para FundBot.
    
    Args:
        name: Nombre del logger
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Archivo opcional para guardar logs
    
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Evitar duplicar handlers
    if logger.handlers:
        return logger
    
    # Formato detallado para logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo si se especifica
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def log_execution_metrics(logger: logging.Logger, start_time: datetime, 
                         portales_count: int, convocatorias_found: int, 
                         relevant_count: int, new_count: int):
    """Log de métricas de ejecución"""
    duration = (datetime.now() - start_time).total_seconds()
    
    logger.info("=== MÉTRICAS DE EJECUCIÓN ===")
    logger.info(f"Duración total: {duration:.2f} segundos")
    logger.info(f"Portales procesados: {portales_count}")
    logger.info(f"Convocatorias encontradas: {convocatorias_found}")
    logger.info(f"Convocatorias relevantes: {relevant_count}")
    logger.info(f"Convocatorias nuevas notificadas: {new_count}")
    
    if portales_count > 0:
        logger.info(f"Promedio por portal: {convocatorias_found/portales_count:.1f} convocatorias")
    
    if convocatorias_found > 0:
        relevance_rate = (relevant_count / convocatorias_found) * 100
        logger.info(f"Tasa de relevancia: {relevance_rate:.1f}%")