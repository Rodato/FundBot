# Portales Sugeridos para Convocatorias de Ciencia de Datos, Visualización e IA

## 🇪🇸 **NACIONALES - ESPAÑA**

### **Organismos Públicos**
- **CDTI** - Centro para el Desarrollo Tecnológico Industrial ✅ *Ya incluido*
- **MINECO** - Ministerio de Ciencia e Innovación ✅ *Ya incluido*
- **IDAE** - Instituto para la Diversificación y Ahorro de la Energía ✅ *Ya incluido*
- **INCIBE** - Instituto Nacional de Ciberseguridad: `https://www.incibe.es/convocatorias`
- **Red.es** - Entidad Pública Empresarial: `https://www.red.es/es/convocatorias-ayudas`
- **SEPE** - Servicio Público de Empleo: `https://www.sepe.es/HomeSepe/empresas/Ayudas-y-subvenciones.html`

### **Financiación Privada**
- **ENISA** - Empresa Nacional de Innovación ✅ *Ya incluido*
- **NEOTEC** - Programa CDTI ✅ *Ya incluido*
- **CaixaBank Dualiza** ✅ *Ya incluido*
- **Banco Santander Innovación**: `https://www.santander.com/es/sostenibilidad/innovacion`
- **BBVA Open Innovation**: `https://www.bbva.com/es/innovacion/`

## 🏛️ **AUTONÓMICOS**

### **Comunidades ya incluidas** ✅
- **Madrid** - Comunidad de Madrid
- **Cataluña** - ACCIÓ (Generalitat)
- **País Vasco** - SPRI
- **Galicia** - IGAPE (Xunta)
- **Andalucía** - Junta de Andalucía

### **Otras Comunidades Relevantes**
- **Valencia** - IVACE: `https://www.ivace.es/index.php/es/ayudas`
- **Castilla y León** - ADE: `https://www.empresas.jcyl.es/web/es/ayudas-empresas.html`
- **Aragón** - IAF: `https://www.iaf.es/ayudas-y-subvenciones/`
- **Murcia** - INFO: `https://www.institutofomentomurcia.es/ayudas`
- **Canarias** - ACIISI: `https://www.cienciacanaria.es/convocatorias/`
- **Asturias** - IDEPA: `https://www.idepa.es/ayudas`

## 🇪🇺 **EUROPEAS**

### **Programas Marco**
- **Horizonte Europa** ✅ *Ya incluido*
- **Digital Europe Programme**: `https://digital-strategy.ec.europa.eu/en/activities/digital-programme`
- **EIT Digital**: `https://www.eitdigital.eu/innovation-entrepreneurship/funding/`
- **EuroHPC**: `https://eurohpc-ju.europa.eu/funding/calls-proposals_en`

### **EIC (European Innovation Council)**
- **EIC Accelerator**: `https://eic.ec.europa.eu/eic-funding-opportunities/eic-accelerator_en`
- **EIC Pathfinder**: `https://eic.ec.europa.eu/eic-funding-opportunities/eic-pathfinder_en`

## 🌍 **INTERNACIONALES**

### **Programas Bilaterales**
- **Programa Iberoeka**: `https://www.cdti.es/index.asp?MP=7&MS=846&MN=2`
- **EUREKA**: `https://www.eurekanetwork.org/`
- **ERA-NET**: Redes europeas de investigación

### **Fondos de Inversión Especializados**
- **Google AI for Social Good**: `https://ai.google/social-good/`
- **Microsoft AI for Good**: `https://www.microsoft.com/en-us/ai/ai-for-good`
- **AWS Credits for Research**: `https://aws.amazon.com/research-credits/`

## 📊 **ESPECIALIZADOS EN DATA & AI**

### **Organizaciones Sector**
- **BigML**: Programa de startups IA
- **IBM Partners Plus**: `https://www.ibm.com/partnerplus/`
- **NVIDIA Inception**: `https://www.nvidia.com/en-us/startups/`
- **Intel AI Builders**: `https://www.intel.com/content/www/us/en/artificial-intelligence/ai-builders.html`

### **Centros Tecnológicos**
- **TECNALIA**: `https://www.tecnalia.com/es/colabora-con-nosotros/convocatorias`
- **CARTIF**: `https://www.cartif.es/proyectos-colaborativos/`
- **ITI**: `https://www.iti.es/colabora/convocatorias/`

## 🎓 **ACADÉMICAS Y UNIVERSIDADES**

### **Centros de Investigación**
- **CSIC**: `https://www.csic.es/es/convocatorias`
- **Agencia Estatal de Investigación**: `https://www.aei.gob.es/convocatorias/`
- **Fundación BBVA**: `https://www.fbbva.es/convocatorias/`

## 🔧 **CÓMO AGREGAR NUEVOS PORTALES**

Para agregar cualquiera de estos portales, simplemente edita `portales.json`:

```json
{
    "nombre-corto": "https://url-del-portal",
    "incibe": "https://www.incibe.es/convocatorias",
    "red-es": "https://www.red.es/es/convocatorias-ayudas"
}
```

El sistema automáticamente:
1. ✅ **Scrapeará** el contenido HTML
2. ✅ **Clasificará** la relevancia para tu empresa
3. ✅ **Filtrará** duplicados
4. ✅ **Generará** resúmenes
5. ✅ **Enviará** notificaciones a Discord

## 📈 **RECOMENDACIONES DE PRIORIDAD**

**ALTA PRIORIDAD** (agregar primero):
1. INCIBE - Muchas convocatorias de IA y ciberseguridad
2. Red.es - Digitalización empresarial
3. IVACE Valencia - Muy activo en tecnología
4. EIC Accelerator - Financiación europea importante

**MEDIA PRIORIDAD**:
- Comunidades autónomas donde operates
- Centros tecnológicos relevantes
- Programas de grandes tech (Google, Microsoft, etc.)

**PARA EVALUAR**:
- URLs que cambien frecuentemente
- Sitios con mucho JavaScript (pueden necesitar ajustes)
- Portales con autenticación requerida