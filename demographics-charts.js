// Funciones para renderizar gráficos demográficos

function renderAgeChartFromAPI(ageData) {
    console.log('📊 Renderizando gráfico de edad:', ageData);
    const ctx = document.getElementById('ageChart');
    if (!ctx) {
        console.error('❌ Canvas ageChart no encontrado');
        return;
    }

    const labels = ageData.map(d => d['Edad del usuario'].replace('Entre ', '').replace(' años', ''));
    const vistas = ageData.map(d => d['Vistas (%)']);
    const retencion = ageData.map(d => d['Porcentaje promedio reproducido (%)']);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Vistas (%)',
                data: vistas,
                backgroundColor: 'rgba(139, 92, 246, 0.8)',
                borderColor: 'rgba(139, 92, 246, 1)',
                borderWidth: 1,
                yAxisID: 'y'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Vistas (%)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Retención (%)'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            }
        }
    });

    console.log('✅ Gráfico de edad renderizado');
}

function renderGenderChartFromAPI(genderData) {
    console.log('📊 Renderizando gráfico de género:', genderData);
    const ctx = document.getElementById('genderChart');
    if (!ctx) {
        console.error('❌ Canvas genderChart no encontrado');
        return;
    }

    const labels = genderData.map(d => d['Género del usuario']);
    const vistas = genderData.map(d => d['Vistas (%)']);

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: vistas,
                backgroundColor: [
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(251, 146, 60, 0.8)'
                ],
                borderColor: [
                    'rgba(59, 130, 246, 1)',
                    'rgba(251, 146, 60, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    console.log('✅ Gráfico de género renderizado');
}

console.log('📦 demographics-charts.js cargado');
