import time
import logging
from functools import wraps
from typing import Any, Callable, Optional, Tuple, Type
import requests

logger = logging.getLogger(__name__)

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator para reintentos con backoff exponencial.
    
    Args:
        max_retries: Número máximo de reintentos
        base_delay: Delay base en segundos
        max_delay: Delay máximo en segundos
        exponential_base: Base para el backoff exponencial
        exceptions: Tupla de excepciones que deben reintentar
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        logger.error(f"Función {func.__name__} falló después de {max_retries} reintentos: {e}")
                        raise e
                    
                    delay = min(base_delay * (exponential_base ** attempt), max_delay)
                    logger.warning(f"Intento {attempt + 1} falló para {func.__name__}: {e}. Reintentando en {delay:.2f}s")
                    time.sleep(delay)
            
            if last_exception:
                raise last_exception
                
        return wrapper
    return decorator

@retry_with_backoff(
    max_retries=3,
    base_delay=2.0,
    exceptions=(requests.RequestException, requests.Timeout, requests.ConnectionError)
)
def robust_http_request(url: str, timeout: int = 20, **kwargs) -> requests.Response:
    """
    Realiza una petición HTTP con reintentos automáticos.
    
    Args:
        url: URL a consultar
        timeout: Timeout en segundos
        **kwargs: Argumentos adicionales para requests.get
    
    Returns:
        Response object
    """
    headers = kwargs.get('headers', {})
    if 'User-Agent' not in headers:
        headers['User-Agent'] = 'Mozilla/5.0 (compatible; FundBot/1.0)'
        kwargs['headers'] = headers
    
    logger.debug(f"Realizando petición HTTP a: {url}")
    response = requests.get(url, timeout=timeout, **kwargs)
    response.raise_for_status()
    
    logger.debug(f"Petición exitosa: {response.status_code} - {len(response.content)} bytes")
    return response