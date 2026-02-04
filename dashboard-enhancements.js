/**
 * Dashboard IdeaPaís - Enhancements
 * Mejoras: ordenamiento de tabla, thumbnails corregidos, Top 20 por fecha
 */

// Estado global para ordenamiento
let currentSortColumn = null;
let currentSortOrder = 'desc';
let allVideosData = [];

/**
 * Override de renderVideosWithThumbnails para usar fecha de publicación
 */
window.renderVideosWithThumbnails = function (contentTable) {
  console.log('🔄 Usando versión mejorada de renderVideosWithThumbnails');

  // Filtrar y guardar todos los videos
  allVideosData = contentTable.filter(v => v.Contenido && v.Contenido !== 'Total');

  // Aplicar filtro de fecha si está activo
  const filterCheckbox = document.getElementById('filterPublishedDate');
  let videosToRender = [...allVideosData];

  if (filterCheckbox && filterCheckbox.checked) {
    // Obtener periodo actual del input
    const periodInput = document.getElementById('periodInput');
    const currentPeriod = periodInput ? periodInput.value : null; // "YYYY-MM"
    if (currentPeriod) {
      const [year, month] = currentPeriod.split('-').map(Number);

      videosToRender = videosToRender.filter(v => {
        const pubDateStr = v['Tiempo de publicación del video'];
        if (!pubDateStr) return false;

        const pubDate = new Date(pubDateStr);
        if (isNaN(pubDate.getTime())) return false; // Fecha inválida

        // Comparar año y mes (ignorar dia y timezone offset issues simple matching)
        // Nota: pubDate es objeto Date local/UTC. "Aug 21, 2025".
        // Mes en JS es 0-indexed
        return pubDate.getFullYear() === year && (pubDate.getMonth() + 1) === month;
      });
    }
  }

  // Ordenar por fecha de publicación (más recientes primero) por defecto
  const sortedVideos = videosToRender.sort((a, b) => {
    const dateA = new Date(a['Tiempo de publicación del video'] || 0);
    const dateB = new Date(b['Tiempo de publicación del video'] || 0);
    return dateB - dateA;
  });

  // Tomar los 20 más recientes
  renderVideosTable(sortedVideos.slice(0, 20));
};

/**
 * Renderiza la tabla de videos con thumbnails
 */
function renderVideosTable(videos) {
  const tbody = document.getElementById('videosTable');
  if (!tbody) {
    console.error('❌ Elemento videosTable no encontrado');
    return;
  }

  tbody.innerHTML = videos.map((video, idx) => {
    const videoId = video.Contenido;
    const videoUrl = `https://www.youtube.com/watch?v=${videoId}`;
    const thumbnail = `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`;
    const title = video['Título del video'] || 'Sin título';
    const pubDate = video['Tiempo de publicación del video'] || '';
    const views = typeof formatNumber === 'function' ? formatNumber(video.Vistas || 0) : (video.Vistas || 0);
    const watchTime = (video['Tiempo de reproducción (horas)'] || 0).toFixed(1);
    const avgPct = (video['Porcentaje promedio reproducido (%)'] || 0).toFixed(1);
    const ctr = (video['Tasa de clics de las impresiones (%)'] || 0).toFixed(2);
    const likes = typeof formatNumber === 'function' ? formatNumber(video['Me gusta'] || 0) : (video['Me gusta'] || 0);
    const shares = typeof formatNumber === 'function' ? formatNumber(video['Elementos compartidos'] || 0) : (video['Elementos compartidos'] || 0);

    const subscribers = (video['Suscriptores'] || 0);

    return `
      <tr>
        <td style="text-align: center; font-weight: 600; color: #6B7280;">${idx + 1}</td>
        <td style="padding: 8px;">
          <a href="${videoUrl}" target="_blank" rel="noopener" title="Ver en YouTube">
            <img src="${thumbnail}" 
                 alt="${escapeHtml(title)}"
                 style="width: 120px; height: 68px; object-fit: cover; border-radius: 8px; display: block; transition: transform 0.2s, box-shadow 0.2s; cursor: pointer;"
                 onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.2)'"
                 onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='none'"
                 onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjY4IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9IiNlNWU3ZWIiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE0IiBmaWxsPSIjOWNhM2FmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+8J+TuTwvdGV4dD48L3N2Zz4='">
          </a>
        </td>
        <td>
          <a href="${videoUrl}" target="_blank" rel="noopener" 
             style="color: #161233; text-decoration: none; font-weight: 500; transition: color 0.2s; display: block;" 
             onmouseover="this.style.color='#3E3CCA'" 
             onmouseout="this.style.color='#161233'">
            ${escapeHtml(title)}
          </a>
          <div style="font-size: 0.75rem; color: #9CA3AF; margin-top: 4px; font-weight: 400;">
            📅 ${pubDate}
          </div>
        </td>
        <td style="text-align: right; font-weight: 500;">${views}</td>
        <td style="text-align: right;">${watchTime}h</td>
        <td style="text-align: right;">${avgPct}%</td>
        <td style="text-align: right; color: ${subscribers > 0 ? '#10B981' : '#6B7280'}; font-weight: 600;">
             ${subscribers > 0 ? '+' : ''}${typeof formatNumber === 'function' ? formatNumber(subscribers) : subscribers}
        </td>
        <td style="text-align: right;">${ctr}%</td>
        <td style="text-align: right;">${likes}</td>
        <td style="text-align: right;">${shares}</td>
      </tr>
    `;
  }).join('');

  console.log(`✅ Renderizados ${videos.length} videos con thumbnails`);
}

/**
 * Ordena la tabla por columna
 */
window.sortVideosBy = function (column) {
  if (!allVideosData || allVideosData.length === 0) {
    console.warn('⚠️ No hay datos de videos para ordenar');
    return;
  }

  // Toggle orden si es la misma columna
  if (currentSortColumn === column) {
    currentSortOrder = currentSortOrder === 'asc' ? 'desc' : 'asc';
  } else {
    currentSortColumn = column;
    currentSortOrder = 'desc'; // Por defecto descendente
  }

  // Ordenar
  const sorted = [...allVideosData].sort((a, b) => {
    let valA, valB;

    if (column === 'Tiempo de publicación del video') {
      valA = new Date(a[column] || 0).getTime();
      valB = new Date(b[column] || 0).getTime();
    } else {
      valA = a[column] || 0;
      valB = b[column] || 0;
    }

    if (currentSortOrder === 'asc') {
      return valA > valB ? 1 : valA < valB ? -1 : 0;
    } else {
      return valA < valB ? 1 : valA > valB ? -1 : 0;
    }
  });

  // Actualizar iconos de ordenamiento en headers
  updateSortIcons(column);

  // Renderizar top 20
  renderVideosTable(sorted.slice(0, 20));

  console.log(`📊 Tabla ordenada por ${column} (${currentSortOrder})`);
};

/**
 * Actualiza los iconos de ordenamiento en los headers
 */
function updateSortIcons(activeColumn) {
  const headers = document.querySelectorAll('th.sortable');
  headers.forEach(th => {
    const column = th.getAttribute('data-column');
    th.classList.remove('asc', 'desc');

    if (column === activeColumn) {
      th.classList.add(currentSortOrder);
    }
  });
}

/**
 * Carga analítica IA desde el servidor
 */
// function loadAIInsights() { ... }
/*
async function loadAIInsights() {
   // ... disabled ...
}
*/
async function loadAIInsights() {
  console.log('🤖 Insights desactivados');
}

/**
 * Carga análisis IA para cada sección del dashboard
 */
// AI Insight loading disabled as per user request
/*
async function loadAllInsights() {
  // ... code removed ...
}
*/

// Function kept empty to prevent errors if called
async function loadAllInsights() {
  console.log('🤖 Análisis IA desactivado');
}

/**
 * Escapa HTML para prevenir XSS
 */
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Hace los headers de la tabla clickeables para ordenar
 */
function makeTableSortable() {
  const headers = [
    { element: document.querySelector('th:nth-child(4)'), column: 'Vistas', label: 'Vistas' },
    { element: document.querySelector('th:nth-child(5)'), column: 'Tiempo de reproducción (horas)', label: 'Tiempo Rep.' },
    { element: document.querySelector('th:nth-child(6)'), column: 'Porcentaje promedio reproducido (%)', label: 'Retención' },
    { element: document.querySelector('th:nth-child(7)'), column: 'Tasa de clics de las impresiones (%)', label: 'CTR' },
    { element: document.querySelector('th:nth-child(8)'), column: 'Me gusta', label: 'Likes' },
    { element: document.querySelector('th:nth-child(9)'), column: 'Elementos compartidos', label: 'Compartidos' }
  ];

  headers.forEach(({ element, column, label }) => {
    if (element) {
      element.classList.add('sortable');
      element.setAttribute('data-column', column);
      element.style.cursor = 'pointer';
      element.style.userSelect = 'none';
      element.title = `Clic para ordenar por ${label}`;

      element.onclick = () => sortVideosBy(column);
    }
  });

  console.log('✅ Tabla configurada para ordenamiento');
}

/**
 * Agrega estilos CSS para ordenamiento
 */
function addSortStyles() {
  if (document.getElementById('sort-styles')) return;

  const style = document.createElement('style');
  style.id = 'sort-styles';
  style.textContent = `
    th.sortable {
      position: relative;
      padding-right: 24px !important;
      transition: background-color 0.2s;
    }
    
    th.sortable:hover {
      background: rgba(62, 60, 202, 0.1) !important;
    }
    
    th.sortable::after {
      content: '↕️';
      position: absolute;
      right: 8px;
      opacity: 0.4;
      font-size: 0.75rem;
    }
    
    th.sortable.asc::after {
      content: '↑';
      opacity: 1;
      color: #3E3CCA;
    }
    
    th.sortable.desc::after {
      content: '↓';
      opacity: 1;
      color: #3E3CCA;
    }
  `;

  document.head.appendChild(style);
}

// Auto-inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', () => {
  console.log('🚀 Dashboard Enhancements cargados');

  // Esperar a que se rendericen los videos y gráficos
  setTimeout(() => {
    addSortStyles();
    makeTableSortable();
    loadAllInsights(); // Cargar insights para todos los gráficos
  }, 2500); // Aumentado a 2.5s para dar tiempo a que cargue
});

console.log('📦 dashboard-enhancements.js cargado');
