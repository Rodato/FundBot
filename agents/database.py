import sqlite3

DB_FILE = "fundbot.db"

def init_db():
    """Crea la tabla de la base de datos si no existe."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS convocatorias (
        url TEXT PRIMARY KEY,
        fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def url_exists(url):
    """Comprueba si una URL ya existe en la base de datos."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM convocatorias WHERE url = ?", (url,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def add_url(url):
    """Añade una nueva URL a la base de datos."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO convocatorias (url) VALUES (?)", (url,))
        conn.commit()
    except sqlite3.IntegrityError:
        # La URL ya existe, no hacemos nada
        pass
    finally:
        conn.close()
