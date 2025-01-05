document.addEventListener("DOMContentLoaded", () => {
    const ctx = document.getElementById("dividendosChart").getContext("2d");

    const mensalRecebidos = JSON.parse(document.getElementById("dividendosChart").dataset.mensalRecebidos);
    const mensalProvisionados = JSON.parse(document.getElementById("dividendosChart").dataset.mensalProvisionados);

    let currentData = mensalRecebidos;
    let chart;

    function renderChart(data) {
        if (chart) chart.destroy();
        const labels = Object.keys(data).sort();
        const values = labels.map((key) => data[key]);

        chart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Dividendos (R$)",
                        data: values,
                        backgroundColor: "rgba(75, 192, 192, 0.2)",
                        borderColor: "rgba(75, 192, 192, 1)",
                        borderWidth: 1,
                    },
                ],
            },
            options: {
                scales: {
                    x: { title: { display: true, text: "Mês" } },
                    y: { title: { display: true, text: "Valor (R$)" } },
                },
            },
        });
    }

    document.getElementById("btnMensalRecebidos").addEventListener("click", () => {
        currentData = mensalRecebidos;
        renderChart(currentData);
    });

    document.getElementById("btnMensalProvisionado").addEventListener("click", () => {
        currentData = mensalProvisionados;
        renderChart(currentData);
    });

    renderChart(currentData);
});
