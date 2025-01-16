// Organiza os dados para o gráfico
const meses = Object.keys(totaisPorMes);
const compras = meses.map((mes) => totaisPorMes[mes].compras);
const vendas = meses.map((mes) => totaisPorMes[mes].vendas);
const bonificacoes = meses.map((mes) => totaisPorMes[mes].bonificacoes);

// Configuração do Chart.js
const ctx = document.getElementById("transacoesChart").getContext("2d");
const transacoesChart = new Chart(ctx, {
    type: "bar",
    data: {
        labels: meses,
        datasets: [
            {
                label: "Compras (R$)",
                data: compras,
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                borderColor: "rgba(75, 192, 192, 1)",
                borderWidth: 1,
            },
            {
                label: "Vendas (R$)",
                data: vendas,
                backgroundColor: "rgba(255, 99, 132, 0.2)",
                borderColor: "rgba(255, 99, 132, 1)",
                borderWidth: 1,
            },
            {
                label: "Bonificações (R$)",
                data: bonificacoes,
                backgroundColor: "rgba(54, 162, 235, 0.2)",
                borderColor: "rgba(54, 162, 235, 1)",
                borderWidth: 1,
            },
        ],
    },
    options: {
        responsive: true,
        plugins: {
            legend: { position: "top" },
            title: {
                display: true,
                text: "Movimentação Mensal",
            },
        },
        scales: {
            x: { title: { display: true, text: "Mês" } },
            y: { title: { display: true, text: "Valor (R$)" } },
        },
    },
});

// Script para manipular a exibição das transações
document.addEventListener("DOMContentLoaded", function () {
    const selectAtivo = document.getElementById("selectAtivo");
    const transacoesAtivos = document.querySelectorAll(".ativo-transacoes");

    // Evento para trocar a exibição ao selecionar um ativo
    selectAtivo.addEventListener("change", function () {
        const ativoSelecionado = this.value;

        // Esconde todas as tabelas de transações
        transacoesAtivos.forEach(div => {
            div.style.display = "none";
        });

        // Mostra a tabela do ativo selecionado
        const ativoDiv = document.getElementById("ativo-" + ativoSelecionado);
        if (ativoDiv) {
            ativoDiv.style.display = "block";
        }
    });
});