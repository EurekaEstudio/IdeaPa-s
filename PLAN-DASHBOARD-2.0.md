# Dashboard IdeaPais 2.0 — Plan de Evolución
> Aplicar a partir de Febrero 2026 (datos de Feb 2026)

## Estado actual (v2.4)
- Dashboard funcional con YouTube dinámico + Meta hardcodeado
- Datos se cargan manualmente desde CSVs exportados
- Varianzas hardcodeadas (corregidas pero no dinámicas)
- Vistas separadas por plataforma: YouTube | Facebook | Instagram
- Desplegado en Easypanel via Docker + Flask

---

## Fase 1: Varianzas dinámicas + limpieza (Esfuerzo: Bajo)

### Qué hacer
- Calcular varianzas automáticamente comparando período actual vs anterior
- Eliminar todos los valores hardcodeados de diff (21.2, 2.9, -26.9, etc.)
- Si no hay mes anterior, no mostrar varianza (ya implementado para Dic)

### Archivos a modificar
- `dashboard-youtube-interactivo.html` línea 793: reemplazar hardcodes con cálculo dinámico desde `windowAllData`

### Lógica
```javascript
const prev = windowAllData[previousPeriod];
const calcVar = (cur, pre) => prev ? ((cur - pre) / pre * 100) : null;
// Usar null para ocultar cuando no hay dato anterior
```

---

## Fase 2: APIs automáticas (Esfuerzo: Medio)

### Opción A: n8n (Recomendada)
- Workflow programado para el día 2 de cada mes
- Nodo YouTube Analytics: consultar KPIs, contenido, tráfico, geografía, demografía
- Nodo Meta Graph API: consultar insights de FB e IG
- Nodo de transformación: mapear a formato JSON actual
- Nodo HTTP/File: guardar JSONs en el servidor o via API

### Opción B: Script Python
- `scripts/fetch_youtube.py` — YouTube Analytics API v3
- `scripts/fetch_meta.py` — Meta Graph API
- Cron job mensual en el servidor
- ~50-80 líneas por script

### Credenciales necesarias
1. **Google Cloud**: Proyecto + OAuth 2.0 + YouTube Analytics API habilitada
2. **Meta for Developers**: App + permisos `pages_read_engagement`, `instagram_basic`, `instagram_manage_insights`
3. **Canal YouTube**: Autorizar OAuth con la cuenta dueña del canal IdeaPaís
4. **Meta pages**: Conectar página FB de IdeaPaís + cuenta IG profesional

### Resultado esperado
- Cero exportación manual de CSVs
- JSONs generados automáticamente cada mes
- Dashboard siempre actualizado

---

## Fase 3: Rediseño de vistas por objetivo (Esfuerzo: Medio)

### Nueva estructura de navegación
```
Resumen Ejecutivo | Alcance | Audiencia | Contenido | [Facebook colapsado]
```

### Vista: Resumen Ejecutivo (NUEVA)
Cruza todas las plataformas en una sola pantalla.

**KPIs principales:**
- Alcance Total (YT views + IG reach + FB reach)
- Engagement Total (likes + comments + shares across all)
- Crecimiento neto (subs YT + followers IG)
- Publicaciones totales (videos + posts + stories)

**Semáforo de salud:**
| Métrica | Valor | Meta | Estado |
|---------|-------|------|--------|
| Audiencia 18-34 en YouTube | actual% | 40% | Rojo/Amarillo/Verde |
| Engagement Instagram | actual% | 3%+ | Color |
| Crecimiento subs YouTube | +N | +30/mes | Color |
| Shares por post Instagram | N | 15+ | Color |

Las metas se definen con IdeaPaís y se ajustan trimestralmente.

### Vista: Alcance
- Gráfico comparativo: YouTube vs Instagram vs Facebook (barras lado a lado)
- Evolución multi-mes (línea de 6-12 meses)
- Fuentes de tráfico YouTube (ya existe)
- Geografía cruzada

### Vista: Audiencia
- Pirámide de edad YouTube (ya existe, darle más protagonismo)
- Gauge: % audiencia joven vs meta
- Género
- Ciudades top (IG + YT combinado)
- Usuarios nuevos vs recurrentes

### Vista: Contenido
- Ranking unificado: mejores posts/videos del mes CRUZANDO plataformas
- Filtro por tipo: Shorts vs Videos largos vs Reels vs Secuencias vs Stories
- Métricas promedio por tipo de contenido
- Tabla Top 20 YouTube (ya existe)

### Vista: Facebook (colapsada/secundaria)
- Dado el 0.13% de engagement, no merece vista completa
- Bloque resumido al final o en la barra lateral
- Si engagement sube de 1%, promover a vista completa

---

## Fase 4: Tendencia multi-mes (Esfuerzo: Medio)

### Qué hacer
- Acumular JSONs históricos (un archivo por mes)
- Gráfico de línea con 6-12 meses para KPIs principales
- Permitir seleccionar rango de fechas

### Estructura de datos
```
/data/
  youtube_2025_12.json
  youtube_2026_01.json
  youtube_2026_02.json
  meta_2026_01.json
  meta_2026_02.json
```

### En el dashboard
- `app.py` escanea la carpeta `/data/` y sirve todos los períodos disponibles
- El frontend construye la línea de tiempo automáticamente

---

## Fase 5: Separar Shorts vs Videos largos (Esfuerzo: Bajo)

### Qué hacer
- Clasificar videos por duración: <= 60 seg = Short, > 60 seg = Estándar
- Mostrar métricas promedio por tipo
- En la tabla Top 20, agregar badge visual "SHORT" o "VIDEO"

### Por qué importa
- Shorts traen 46% del tráfico pero diferente audiencia
- Los largos tienen mejor retención y más subs
- Necesitan saber qué formato priorizar según el objetivo

---

## Cronograma sugerido

| Mes | Fase | Entregable |
|-----|------|-----------|
| Feb 2026 | Fase 1 | Varianzas dinámicas + datos Feb procesados |
| Feb 2026 | Fase 5 | Shorts vs Videos largos en tabla |
| Mar 2026 | Fase 2 | APIs automáticas funcionando |
| Mar 2026 | Fase 4 | Tendencia 3 meses (Dic-Ene-Feb) |
| Abr 2026 | Fase 3 | Rediseño completo de vistas |

---

## Métricas de éxito del dashboard mismo
- Tiempo de generación del reporte: de 60 min manual a 0 min automático
- Errores de datos: de posibles (como el +15.4%) a cero (cálculos dinámicos)
- Tiempo para entender el estado: de "leer todo" a 10 segundos (resumen ejecutivo)

---

## Stack técnico
- **Frontend**: HTML + Chart.js (mantener, funciona bien)
- **Backend**: Flask/Python (mantener)
- **Automatización**: n8n o cron + scripts Python
- **Deploy**: Easypanel + Docker (mantener)
- **Datos**: JSONs en servidor (migrar a carpeta /data/ organizada)
