# Proyecto: Dashboards Analytics IdeaPaís

> Documento de contexto para continuidad del proyecto
> Última actualización: 4 de febrero de 2026

---

## 1. Resumen Ejecutivo

Este proyecto tiene como objetivo crear un sistema de **dashboards interactivos** para visualizar métricas de redes sociales de **IdeaPaís**, una organización chilena que celebra 15 años de trayectoria.

### Plataformas objetivo:
- **YouTube Analytics** ✅ (Completado)
- **Meta Business Suite** (Instagram/Facebook) 🔄 (Skill creada, pendiente datos)

### Entregables creados:
1. **Dashboard HTML interactivo** - Aplicación web standalone para cargar CSV y generar dashboards
2. **Sistema de Skills** - Habilidades de Claude Code para automatizar la generación
3. **Sistema de comparativas mensuales** - Almacenamiento local para tracking mes a mes

---

## 2. Estructura del Proyecto

```
/Volumes/External WW/Proyectos VS Code/Dashboard Idea País/
│
├── 📄 dashboard-youtube-interactivo.html    # Dashboard principal (aplicación web)
├── 📄 PROYECTO-DASHBOARDS-IDEAPAIS.md       # Este documento
├── 🖼️ Logo a color sobre fondo blanco.png   # Logo IdeaPaís (15 años)
├── 📕 Manual IP.pdf                          # Manual de marca (23MB, no procesable directamente)
│
├── 📁 .claude/skills/                        # Skills de Claude Code
│   ├── 📁 dashboard-youtube/
│   │   ├── SKILL.md                          # Instrucciones para generar dashboard YouTube
│   │   └── template.html                     # Template HTML base
│   ├── 📁 dashboard-meta/
│   │   ├── SKILL.md                          # Instrucciones para dashboard Meta
│   │   └── template.html                     # Template HTML para Meta
│   ├── 📁 ideapais-brand/
│   │   └── SKILL.md                          # Guía de marca y colores
│   └── 📁 csv-dashboard-generator/
│       └── SKILL.md                          # Skill principal orquestadora
│
├── 📁 Fuente de tráfico 2026-01-01_2026-02-01 IdeaPais/
│   ├── Datos del gráfico.csv                 # Series temporales por fuente
│   ├── Datos de la tabla.csv                 # Resumen por fuente de tráfico
│   └── Totales.csv                           # Vistas diarias totales
│
├── 📁 Área geográfica 2026-01-01_2026-02-01 IdeaPais/
│   ├── Datos del gráfico.csv                 # Series temporales por país
│   ├── Datos de la tabla.csv                 # Resumen por país
│   └── Totales.csv                           # Vistas diarias totales
│
└── 📁 Contenido 2026-01-01_2026-02-01 IdeaPais (full)/
    ├── Datos del gráfico.csv                 # Series temporales por video
    ├── Datos de la tabla.csv                 # Métricas detalladas por video
    └── Totales.csv                           # Vistas diarias totales
```

---

## 3. Datos de YouTube Analytics

### 3.1 Estructura de CSV - Fuente de Tráfico

**Archivo: `Datos de la tabla.csv`**

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| Fuente de tráfico | Origen de las vistas | "Búsqueda de YouTube" |
| Vistas | Número total de vistas | 1109 |
| Tiempo de reproducción (horas) | Horas totales vistas | 77.0998 |
| Duración promedio de vistas | Tiempo promedio por vista | "0:04:36" |
| Impresiones | Veces que se mostró el video | 15666 |
| Tasa de clics de las impresiones (%) | CTR | 5.68 |

**Fuentes de tráfico identificadas (Enero 2026):**
- Feed de Shorts (3.757 vistas - 46%)
- Búsqueda de YouTube (1.109 vistas)
- Videos sugeridos (953 vistas)
- Externas (892 vistas)
- Funciones de exploración (812 vistas)
- Directa o desconocida (323 vistas)
- Canales de usuario (151 vistas)
- Otras funciones de YouTube (77 vistas)
- Notificaciones (24 vistas)
- Playlists (19 vistas)

### 3.2 Estructura de CSV - Área Geográfica

**Archivo: `Datos de la tabla.csv`**

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| Ubicación geográfica | Código de país | "CL" |
| Vistas | Número total de vistas | 3922 |
| Tiempo de reproducción (horas) | Horas totales | 253.67 |
| Duración promedio de vistas | Tiempo promedio | "0:04:41" |

**Top países (Enero 2026):**
1. Chile (CL) - 3.922 vistas (48%)
2. España (ES) - 612 vistas
3. Estados Unidos (US) - 290 vistas
4. México (MX) - 262 vistas
5. Venezuela (VE) - 233 vistas

### 3.3 Estructura de CSV - Contenido (Videos)

**Archivo: `Datos de la tabla.csv`**

| Columna | Descripción | Uso en Dashboard |
|---------|-------------|------------------|
| Contenido | ID del video de YouTube | Identificador único |
| Título del video | Nombre del video | Mostrar en rankings/tabla |
| Tiempo de publicación del video | Fecha de publicación | Contexto |
| Duración | Duración del video en segundos | Contexto |
| **Porcentaje promedio reproducido (%)** | **RETENCIÓN** | KPI + Ranking |
| Se quedaron para mirar (%) | Retención inicial | Análisis |
| Usuarios únicos | Viewers únicos | Análisis |
| Vistas promedio por usuario | Replay rate | Análisis |
| **Suscriptores obtenidos** | Nuevos subs del video | KPI + Ranking |
| Suscriptores perdidos | Bajas del video | KPI (neto) |
| **Me gusta** | Likes | Engagement |
| No me gusta | Dislikes | Engagement |
| **Elementos compartidos** | Shares | Ranking |
| Comentarios agregados | Comments | Engagement |
| **Vistas** | Total de vistas | KPI + Ranking |
| Tiempo de reproducción (horas) | Watch time | KPI |
| Impresiones | Veces mostrado | CTR cálculo |
| **Tasa de clics de las impresiones (%)** | **CTR** | KPI + Ranking |

### 3.4 Métricas Totales (Enero 2026)

| Métrica | Valor |
|---------|-------|
| Vistas totales | 8.120 |
| Tiempo de reproducción | 355,28 horas |
| Suscriptores netos | +19 (26 ganados - 7 perdidos) |
| CTR promedio | 2,68% |
| Retención promedio | 17,85% |
| Impresiones totales | 83.263 |

---

## 4. Skills de Claude Code

### 4.1 `/dashboard-youtube`

**Propósito:** Generar dashboard HTML de YouTube Analytics

**Invocación manual:** Sí (disable-model-invocation: true)

**KPIs que genera:**
1. Vistas Totales
2. Horas de Reproducción
3. Suscriptores Netos
4. CTR Promedio
5. Retención Promedio
6. Engagement Rate

**Rankings Top 3:**
1. Más Vistas
2. Mejor CTR (filtra ≥100 impresiones)
3. Mayor Retención (filtra ≥10 vistas)
4. Más Compartidos
5. Ganadores de Suscriptores

**Gráficos:**
- Tendencia de vistas diarias (línea)
- Fuentes de tráfico (barras horizontales)
- Distribución geográfica (dona)

### 4.2 `/dashboard-meta`

**Propósito:** Generar dashboard HTML de Instagram/Facebook

**Estado:** Skill creada, pendiente de datos CSV de Meta

**KPIs planificados:**
1. Alcance Total
2. Impresiones
3. Engagement Rate
4. Nuevos Seguidores

### 4.3 `ideapais-brand` (automática)

**Propósito:** Proporcionar directrices de marca a Claude

**Invocación:** Automática cuando Claude lo necesita

**Contenido:**
- Colores de marca
- Tipografía
- Estilos de componentes
- Configuración de Chart.js

### 4.4 `/csv-dashboard-generator`

**Propósito:** Detectar tipo de CSV y generar dashboard apropiado

**Funcionalidad:**
1. Escanea CSVs en el proyecto
2. Identifica origen (YouTube/Meta)
3. Delega a skill específica

---

## 5. Colores de Marca IdeaPaís

### Colores Principales

```css
/* Primario */
--primary: #1E1E3F;        /* Azul oscuro IdeaPaís */
--primary-light: #2D2D5A;  /* Hover states */
--primary-lighter: #4A4A7A; /* Elementos secundarios */

/* Neutros */
--white: #FFFFFF;
--gray-50: #F9FAFB;
--gray-100: #F5F5F7;        /* Fondo principal */
--gray-200: #E5E7EB;        /* Bordes */
--gray-500: #6B7280;        /* Texto secundario */

/* Estados */
--positive: #10B981;        /* Verde - mejoras */
--negative: #EF4444;        /* Rojo - caídas */
```

### Paleta para Gráficos

```javascript
const colors = [
  '#1E1E3F',  // Azul oscuro (primario)
  '#3B82F6',  // Azul brillante
  '#10B981',  // Verde esmeralda
  '#F59E0B',  // Amarillo/naranja
  '#EF4444',  // Rojo
  '#8B5CF6',  // Púrpura
  '#EC4899',  // Rosa
  '#14B8A6',  // Teal
  '#6366F1',  // Índigo
  '#84CC16',  // Lima
  '#F97316',  // Naranja
  '#06B6D4'   // Cyan
];
```

---

## 6. Dashboard Interactivo

### 6.1 Archivo Principal

**Ubicación:** `dashboard-youtube-interactivo.html`

**Características:**
- Aplicación web standalone (un solo archivo HTML)
- No requiere servidor
- Funciona offline
- Usa Chart.js desde CDN

### 6.2 Funcionalidades

#### Carga de Archivos
- Zona de drag & drop
- Detección automática de tipo de archivo
- Soporte para múltiples archivos simultáneos
- Validación de formato CSV

#### Procesamiento
- Parser CSV en JavaScript (maneja formato español)
- Cálculo automático de KPIs
- Generación de rankings con filtros anti-outliers
- Renderizado dinámico de gráficos

#### Almacenamiento Local
- Guarda datos en `localStorage` del navegador
- Clave: `ytDashboardData`
- Estructura por período (YYYY-MM)
- Permite cargar períodos anteriores

#### Comparativas Mensuales
- Detecta automáticamente el mes anterior
- Calcula variación porcentual
- Muestra indicadores visuales (▲/▼)
- Badge "Mes base" cuando no hay comparativa

#### Exportación
- Botón "Exportar PDF" (window.print())
- Estilos de impresión optimizados
- Oculta controles en impresión

### 6.3 Flujo de Uso

```
1. Abrir dashboard-youtube-interactivo.html en navegador
                    ↓
2. Arrastrar archivos CSV a la zona de carga
   - Datos de la tabla.csv (Fuente de tráfico)
   - Datos de la tabla.csv (Área geográfica)
   - Datos de la tabla.csv (Contenido)
   - Totales.csv
                    ↓
3. Seleccionar período (mes/año)
                    ↓
4. Clic en "Procesar y generar dashboard"
                    ↓
5. Dashboard se genera automáticamente
   - KPIs calculados
   - Gráficos renderizados
   - Rankings ordenados
   - Tabla de videos poblada
                    ↓
6. Datos guardados en localStorage
                    ↓
7. Próximo mes: repetir proceso
   - Sistema detecta mes anterior
   - Genera comparativas automáticas
```

### 6.4 Estructura de Datos en localStorage

```javascript
{
  "2026-01": {
    "traffic": [...],      // Datos de fuente de tráfico
    "geo": [...],          // Datos geográficos
    "content": [...],      // Datos de videos
    "totals": [...],       // Totales diarios
    "savedAt": "2026-02-04T..."
  },
  "2026-02": {
    // Datos del siguiente mes
  }
}
```

---

## 7. Fórmulas y Cálculos

### KPIs

```javascript
// Vistas Totales
totalViews = SUM(traffic.Vistas) donde Fuente="Total"

// Horas de Reproducción
totalWatchTime = SUM(traffic["Tiempo de reproducción (horas)"]) donde Fuente="Total"

// Suscriptores Netos
netSubs = SUM(content["Suscriptores obtenidos"]) - SUM(content["Suscriptores perdidos"])

// CTR Promedio (de la fila Total de tráfico)
avgCTR = traffic["Tasa de clics de las impresiones (%)"] donde Fuente="Total"

// Retención Promedio
avgRetention = AVG(content["Porcentaje promedio reproducido (%)"])
               donde "Título del video" != null

// Engagement Rate
engagementRate = ((totalLikes + totalComments + totalShares) / totalViews) * 100
```

### Variación Mensual

```javascript
variacion = ((valorActual - valorAnterior) / valorAnterior) * 100

// Mostrar como:
// ▲ +15.3% (verde) si positivo
// ▼ -8.2% (rojo) si negativo
// — Mes base (gris) si no hay anterior
```

### Filtros Anti-Outliers para Rankings

```javascript
// Top CTR: Solo videos con >= 100 impresiones
topCTR = content.filter(v => v.Impresiones >= 100)
                .sort((a,b) => b.CTR - a.CTR)
                .slice(0, 3)

// Top Retención: Solo videos con >= 10 vistas
topRetention = content.filter(v => v.Vistas >= 10)
                      .sort((a,b) => b.Retencion - a.Retencion)
                      .slice(0, 3)
```

---

## 8. Próximos Pasos

### Inmediatos
- [ ] Probar dashboard con datos de enero 2026
- [ ] Ajustar filtros si hay outliers
- [ ] Verificar formato de números chileno

### Corto Plazo
- [ ] Obtener CSV de Meta Business Suite (Instagram/Facebook)
- [ ] Adaptar dashboard-meta con datos reales
- [ ] Crear dashboard unificado (YouTube + Meta)

### Mejoras Futuras
- [ ] Agregar gráfico de rendimiento Shorts vs Videos largos
- [ ] Implementar exportación a Excel
- [ ] Agregar análisis de mejores horarios de publicación
- [ ] Integrar con API de YouTube (automatizar descarga)
- [ ] Crear versión con backend para múltiples usuarios

---

## 9. Notas Técnicas

### Parseo de CSV

El parser maneja:
- Encoding UTF-8
- Separador coma (,)
- Valores entre comillas
- Formato numérico español (1.234,56)

```javascript
// Conversión de número español a JavaScript
function parseNumber(str) {
  const cleaned = str.replace(/\./g, '').replace(',', '.');
  return parseFloat(cleaned);
}
```

### Chart.js

Versión: Última disponible via CDN
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

Configuración común:
```javascript
const commonOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: { usePointStyle: true }
    }
  }
};
```

### Compatibilidad

- Chrome: ✅ Completo
- Firefox: ✅ Completo
- Safari: ✅ Completo
- Edge: ✅ Completo
- IE11: ❌ No soportado

---

## 10. Archivos de Referencia

### Logo
- **Archivo:** `Logo a color sobre fondo blanco.png`
- **Uso:** Header del dashboard
- **Dimensiones recomendadas:** height: 45px

### Manual de Marca
- **Archivo:** `Manual IP.pdf`
- **Tamaño:** 23MB (muy grande para procesamiento directo)
- **Contenido:** Guías de identidad visual completas

---

## 11. Comandos Útiles

### Abrir Dashboard
```bash
open "dashboard-youtube-interactivo.html"
```

### Listar Skills
```bash
ls -la .claude/skills/
```

### Ver estructura de CSV
```bash
head -5 "Fuente de tráfico 2026-01-01_2026-02-01 IdeaPais/Datos de la tabla.csv"
```

---

## 12. Contacto y Soporte

**Organización:** IdeaPaís
**Website:** https://ideapais.cl

---

*Documento generado para continuidad de proyecto con Claude Code*
*Versión: 1.0*
*Fecha: 4 de febrero de 2026*
