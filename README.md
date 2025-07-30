# FundBot 🇨🇴

FundBot es un bot automatizado diseñado para encontrar, filtrar y notificar sobre convocatorias de financiación relevantes para **empresas colombianas especializadas en Ciencia de Datos, Visualización de Datos e Inteligencia Artificial**.

## 🚀 Características

-   **🧠 Scraping Inteligente:** Utiliza Gemini 2.0 Flash para extraer convocatorias de portales colombianos e internacionales, adaptándose a diferentes estructuras HTML.
-   **🎯 Clasificación Geográfica:** Filtra automáticamente convocatorias **elegibles para empresas colombianas**, excluyendo programas regionales restrictivos.
-   **🏢 Perfil Especializado:** Configurado específicamente para empresas de **Data Science, Visualización de Datos e IA**.
-   **📊 Resúmenes Ejecutivos:** Genera resúmenes concisos enfocados en elegibilidad, fechas límite y relevancia para tu sector.
-   **💬 Notificaciones Discord:** Envía alertas con colores distintivos por fuente (🟡 MinCiencias, 🟢 Fondos Internacionales).
-   **🔄 Sistema Robusto:** Logging detallado, reintentos automáticos y manejo de errores resiliente.
-   **🗄️ Base de Datos Inteligente:** SQLite con estadísticas, deduplicación y tracking de fuentes.
-   **⏰ Automatización 24/7:** Ejecución diaria automática via GitHub Actions.

## 🔄 Cómo Funciona

1.  **🌐 Carga de Portales:** Carga portales colombianos e internacionales desde `portales.json`
2.  **🕷️ Scraping Inteligente:** Extrae convocatorias usando IA, con reintentos automáticos y manejo de errores
3.  **🇨🇴 Clasificación Geográfica:** Evalúa elegibilidad para empresas colombianas y relevancia sectorial
4.  **🔍 Filtrado de Duplicados:** Verifica contra base de datos histórica para evitar repeticiones
5.  **📝 Generación de Resúmenes:** Crea resúmenes ejecutivos con fechas límite y criterios de aplicación
6.  **📱 Notificación Discord:** Envía alertas organizadas por colores según la fuente
7.  **💾 Persistencia:** Almacena resultados con metadata completa para análisis y estadísticas

## ⚙️ Configuración Local

### 🚀 Instalación Rápida

```bash
# 1. Clona el repositorio
git clone https://github.com/Rodato/FundBot.git
cd FundBot

# 2. Configura entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Configura credenciales (ver abajo)
cp .env.example .env
# Edita .env con tus claves

# 5. Ejecuta pruebas del sistema
python test_system.py

# 6. Ejecuta el bot
python main.py
```

### 🔑 Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
# APIs requeridas
GOOGLE_API_KEY="tu_api_key_de_gemini_aqui"
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/tu_webhook_aqui"

# Configuración opcional
LOG_LEVEL="INFO"        # DEBUG para más detalle
LOG_FILE="logs/fundbot.log"
```

**📋 Cómo obtener las claves:**
- **Google API Key**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Discord Webhook**: Servidor Discord > Configuración Canal > Integraciones > Webhooks

## 🌐 Configuración de Portales

### 📋 Portales Actuales

```json
{
    "minciencias-colombia": "https://minciencias.gov.co/convocatorias/todas",
    "fondation-botnar": "https://www.fondationbotnar.org/funding-opportunities/"
}
```

### 🎯 Portales Recomendados para Colombia

**🥇 Alta Prioridad:**
- **iNNpulsa Colombia**: Innovación empresarial
- **SENA Fondo Emprender**: Emprendimiento tecnológico  
- **BID Lab**: Laboratorio de innovación del BID
- **Google AI for Social Good**: Programa global de IA

**🥈 Media Prioridad:**
- **Ruta N Medellín**: Ecosistema de innovación
- **Horizonte Europa**: Programas internacionales UE
- **CAF**: Banco de Desarrollo de América Latina

Ver `portales_colombia_internacional.md` para **40+ fuentes adicionales** categorizadas por elegibilidad.

## ⏰ Automatización con GitHub Actions

### 🔄 Configuración del Workflow

**⏰ Ejecución Automática:** Todos los días a las **08:00 UTC** (3:00 AM hora Colombia)
**🔧 Ejecución Manual:** Desde GitHub > Actions > "Run workflow"

### 🔐 Configuración de Secrets

En tu repositorio GitHub: `Settings` > `Secrets and variables` > `Actions`

```
GOOGLE_API_KEY = tu_api_key_de_gemini
DISCORD_WEBHOOK_URL = tu_webhook_de_discord
```

### ⚙️ Permisos Requeridos

`Settings` > `Actions` > `General` > `Workflow permissions`:
- ✅ **"Read and write permissions"** (para commits automáticos de la BD)

---

## 🎯 Para Empresas Colombianas

### ✅ Eligibilidad Automática
FundBot está **configurado específicamente** para:
- 🇨🇴 **Empresas ubicadas en Colombia**
- 📊 **Sector Data Science, Visualización e IA**  
- 🌎 **Convocatorias internacionales abiertas**
- ❌ **Excluye automáticamente** programas regionales restrictivos

### 🏢 Perfil de Empresa
- **Ciencia de datos** y análisis avanzado
- **Visualización** y dashboards interactivos
- **IA y Machine Learning** 
- **Big Data** y procesamiento masivo
- **Business Intelligence** empresarial

### 🔍 Fuentes Priorizadas
1. **🟡 MinCiencias Colombia** - Convocatorias nacionales
2. **🟢 Fundaciones Internacionales** - Impacto social y tecnología
3. **🔵 Programas Europeos** - Solo los abiertos internacionalmente
4. **🔴 Organismos Multilaterales** - BID, Banco Mundial, etc.

---

## 📊 Características Avanzadas

### 🧠 Sistema Inteligente
- **Reintentos automáticos** con backoff exponencial
- **Logging estructurado** con métricas detalladas
- **Validación de datos** en cada etapa
- **Manejo de errores** resiliente

### 📈 Monitoreo y Estadísticas
- **Base de datos** con histórico completo
- **Métricas de ejecución** y rendimiento
- **Tracking por fuente** y tipo de convocatoria
- **Logs configurables** (DEBUG/INFO/WARNING/ERROR)

### 🎨 Notificaciones Personalizadas
- **Colores por fuente** para fácil identificación
- **Embeds ricos** con metadata completa
- **Rate limiting** inteligente para Discord
- **Timestamps** y footer informativos

---

## 📚 Documentación Adicional

- **`CLAUDE.md`**: Guía completa para Claude Code
- **`portales_colombia_internacional.md`**: 40+ fuentes adicionales
- **`test_system.py`**: Suite de pruebas integral
- **`.env.example`**: Plantilla de configuración

---

## 🤝 Contribuciones

¿Conoces portales de financiación relevantes para empresas colombianas de IA/Data Science? 

1. Fork del repositorio
2. Agrega el portal a `portales.json`
3. Ejecuta las pruebas: `python test_system.py`
4. Crea un Pull Request

**Criterios de elegibilidad:**
- ✅ Abierto a empresas colombianas
- ✅ Relevante para Data Science/IA
- ✅ URL estable y scrapeables
- ❌ No requiere residencia europea exclusiva
