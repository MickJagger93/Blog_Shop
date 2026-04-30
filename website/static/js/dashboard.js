let searchChartInstance; 

const initDashboardCharts = (config) => {
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                labels: { color: 'white', font: { size: 12 } }
            }
        }
    };

    const ctxSearch = document.getElementById('searchChart');
    if (ctxSearch) {
        
        searchChartInstance = new Chart(ctxSearch, {
            type: 'bar',
            data: {
                labels: config.searchLabels,
                datasets: [
                    {
                        label: 'Buscados',
                        data: config.searchData,
                        backgroundColor: 'rgba(75, 192, 192, 0.7)', 
                        borderColor: '#4bc0c0',
                        borderWidth: 1,
                        hidden: false
                    },
                    {
                        label: 'Vendidos',
                        data: config.vendidosData,
                        backgroundColor: 'rgba(46, 204, 113, 0.7)', 
                        borderColor: '#2ecc71',
                        borderWidth: 1,
                        hidden: false
                    },
                    {
                        label: 'En Carrito',
                        data: config.carritoData,
                        backgroundColor: 'rgba(231, 76, 60, 0.7)', 
                        borderColor: '#e74c3c',
                        borderWidth: 1,
                        hidden: false
                    }
                ]
            },
            options: {
                ...commonOptions,
                scales: {
                    y: { 
                        beginAtZero: true, 
                        ticks: { color: 'white' },
                        grid: { color: 'rgba(255,255,255,0.1)' }
                    },
                    x: { 
                        ticks: { color: 'white' },
                        grid: { display: false }
                    }
                }
            }
        });
    }

    const ctxPosts = document.getElementById('postChart');
    if (ctxPosts) {
        new Chart(ctxPosts, {
            type: 'doughnut',
            data: {
                labels: config.postLabels,
                datasets: [{
                    data: config.postData,
                    backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe', '#ffce56', '#2ecc71'],
                    hoverOffset: 10
                }]
            },
            options: {
                ...commonOptions,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: 'white' }
                    }
                }
            }
        });
    }
};

window.updateChart = () => {
    if (!searchChartInstance) return;
    
    // El índice 0 es Buscados, 1 es Vendidos, 2 es Carrito
    searchChartInstance.setDatasetVisibility(0, document.getElementById('check-buscados').checked);
    searchChartInstance.setDatasetVisibility(1, document.getElementById('check-vendidos').checked);
    searchChartInstance.setDatasetVisibility(2, document.getElementById('check-carrito').checked);
    
    searchChartInstance.update();
};

document.addEventListener('DOMContentLoaded', () => {
    const searchDataEl = document.getElementById('search-labels-data');
    
    if (searchDataEl) {
        const dashboardData = {
            searchLabels: JSON.parse(document.getElementById('search-labels-data').textContent),
            searchData: JSON.parse(document.getElementById('search-data-data').textContent),
            // Nuevos datos
            vendidosData: JSON.parse(document.getElementById('vendidos-data').textContent),
            carritoData: JSON.parse(document.getElementById('carrito-data').textContent),
            // Datos de posts
            postLabels: JSON.parse(document.getElementById('post-labels-data').textContent),
            postData: JSON.parse(document.getElementById('post-data-data').textContent)
        };
       
        initDashboardCharts(dashboardData);
    }
});

function generarReportePDF() {
    const elemento = document.querySelector(".dashboard-container");
    
    // 1. Cambiamos colores de los gráficos a NEGRO para el PDF
    const charts = Chart.instances;
    Object.values(charts).forEach(chart => {
        chart.options.plugins.legend.labels.color = 'black';
        if (chart.options.scales && chart.options.scales.y) {
            chart.options.scales.y.ticks.color = 'black';
            chart.options.scales.x.ticks.color = 'black';
        }
        chart.update('none'); // Update sin animaciones
    });

    elemento.classList.add("modo-pdf");

    const opciones = {
        margin: [10, 10],
        filename: 'reporte_analisis.pdf',
        image: { type: 'jpeg', quality: 1 },
        html2canvas: { scale: 2, useCORS: true, backgroundColor: '#ffffff' },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
        pagebreak: { mode: ['css', 'legacy'] }
    };

    html2pdf().set(opciones).from(elemento).save().then(() => {
        // 2. Restauramos colores a BLANCO para la web
        elemento.classList.remove("modo-pdf");
        Object.values(charts).forEach(chart => {
            chart.options.plugins.legend.labels.color = 'white';
            if (chart.options.scales && chart.options.scales.y) {
                chart.options.scales.y.ticks.color = 'white';
                chart.options.scales.x.ticks.color = 'white';
            }
            chart.update('none');
        });
    });
}

function toggleDashboardSection(className, checkbox) {
    const section = document.querySelector('.' + className);
    if (section) {
        section.style.display = checkbox.checked ? '' : 'none';
    }
}
