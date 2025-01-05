const ctx = document.getElementById('graficoPizza').getContext('2d');

if (typeof alocacoesJson !== 'undefined') {
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(alocacoesJson),
            datasets: [{
                data: Object.values(alocacoesJson),
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF', '#FF5733', '#33FF57', '#3357FF'],
            }]
        },
        options: {
            responsive: true,
        }
    });
} else {
    console.error("Variável 'alocacoesJson' não definida.");
}