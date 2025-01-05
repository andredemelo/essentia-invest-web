// Configuração do gráfico
var ctx = document.getElementById('graficoPizza').getContext('2d');
var graficoPizza = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: nomesAtivos,
        datasets: [{
            data: notasAtivos,
            backgroundColor: [
                '#FF6384',
                '#36A2EB',
                '#FFCE56',
                '#4BC0C0',
                '#9966FF',
                '#FF9F40',
                '#C9CBCF',
                '#FF5733',
                '#33FF57',
                '#3357FF'
            ],
        }]
    },
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        var valor = tooltipItem.raw;
                        var percentual = ((valor / soma_notas) * 100).toFixed(2);
                        return nomesAtivos[tooltipItem.dataIndex] + ': ' + percentual + '%';
                    }
                }
            }
        }
    }
});