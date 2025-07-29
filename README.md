# FundBot

FundBot es un bot automatizado diseñado para encontrar, filtrar y notificar sobre convocatorias de financiación relevantes para una empresa especializada en Inteligencia Artificial, visualización de datos y dashboards.

## Características

-   **Scraping Inteligente:** Utiliza un modelo de lenguaje (Gemini 2.0 Flash) para extraer convocatorias de financiación de diversas páginas web, adaptándose a diferentes estructuras HTML.
-   **Clasificación con IA:** Filtra las convocatorias encontradas para identificar solo aquellas que son relevantes para el perfil de la empresa, utilizando un modelo de IA.
-   **Resumen Automático:** Genera resúmenes concisos de las convocatorias relevantes, destacando la información clave.
-   **Notificaciones por Discord:** Envía las convocatorias relevantes y resumidas directamente a un canal de Discord.
-   **Persistencia de Datos:** Utiliza una base de datos SQLite (`fundbot.db`) para almacenar las URLs de las convocatorias ya procesadas, evitando notificaciones duplicadas.
-   **Configuración Externa:** La lista de portales web a escanear se gestiona fácilmente a través de un archivo JSON externo (`portales.json`).
-   **Automatización Diaria:** Configurado para ejecutarse automáticamente cada día mediante GitHub Actions.

## Cómo Funciona

1.  **Carga de Portales:** Lee la lista de URLs de `portales.json`.
2.  **Scraping:** Visita cada URL, descarga el contenido HTML y utiliza Gemini 2.0 Flash para extraer títulos, URLs y resúmenes de posibles convocatorias.
3.  **Clasificación:** Pasa las convocatorias extraídas por un segundo modelo de Gemini 2.0 Flash para determinar si son relevantes para el perfil de la empresa.
4.  **Filtrado de Duplicados:** Comprueba en `fundbot.db` si la convocatoria ya ha sido notificada previamente.
5.  **Resumen:** Para las convocatorias nuevas y relevantes, un tercer modelo de Gemini 2.0 Flash genera un resumen conciso.
6.  **Notificación:** Envía los resúmenes de las nuevas convocatorias a Discord.
7.  **Almacenamiento:** Guarda las URLs de las convocatorias notificadas en `fundbot.db` para futuras ejecuciones.

## Configuración Local

Para ejecutar FundBot en tu entorno local:

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/Rodato/FundBot.git
    cd FundBot
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura tus credenciales:**
    Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido, reemplazando los valores con tus propias claves:
    ```
    GOOGLE_API_KEY="TU_API_KEY_DE_GOOGLE"
    DISCORD_WEBHOOK_URL="TU_WEBHOOK_DE_DISCORD"
    ```

5.  **Ejecuta el bot (prueba):**
    ```bash
    python main.py
    ```

## Configuración de Portales

Para añadir o eliminar portales web que el bot debe escanear, edita el archivo `portales.json` en la raíz del proyecto. El formato es un objeto JSON donde la clave es un nombre descriptivo para el portal y el valor es su URL.

```json
{
    "cdti": "https://www.cdti.es/es/convocatorias",
    "red.es": "https://www.red.es/es/buscador-de-ayudas",
    "accio": "https://www.accio.gencat.cat/ca/ajuts/"
}
```

## Automatización con GitHub Actions

FundBot está configurado para ejecutarse diariamente a través de GitHub Actions. El workflow se define en `.github/workflows/daily_scraper.yml`.

Para que la automatización funcione correctamente, debes configurar lo siguiente en tu repositorio de GitHub:

1.  **Secrets del Repositorio:**
    Ve a `Settings` > `Secrets and variables` > `Actions` y añade los siguientes secretos:
    -   `GOOGLE_API_KEY`: Tu clave de API de Google.
    -   `DISCORD_WEBHOOK_URL`: La URL de tu webhook de Discord.

2.  **Permisos del Workflow:**
    Ve a `Settings` > `Actions` > `General` > `Workflow permissions` y selecciona `Read and write permissions`. Esto permite que el workflow pueda hacer `commit` y `push` de la base de datos `fundbot.db` actualizada.

El workflow se ejecutará automáticamente cada día a las 08:00 UTC. También puedes activarlo manualmente desde la pestaña `Actions` de tu repositorio en GitHub.
