// Script para o gráfico de dividendos
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

// Script para manipular a exibição dos dividendos conforme a seleção do ativo
document.addEventListener("DOMContentLoaded", function () {
    const selectAtivo = document.getElementById("selectAtivo");
    const dividendosAtivos = document.querySelectorAll(".ativo-dividendos");

    // Evento para trocar a exibição ao selecionar um ativo
    selectAtivo.addEventListener("change", function () {
        const ativoSelecionado = this.value;

        // Esconde todas as tabelas de dividendos
        dividendosAtivos.forEach(div => {
            div.style.display = "none";
        });

        // Mostra a tabela do ativo selecionado
        const ativoDiv = document.getElementById("ativo-" + ativoSelecionado);
        if (ativoDiv) {
            ativoDiv.style.display = "block";
        }
    });
});

// Script para filtrar dividendos por mês
document.getElementById("btnFiltrar").addEventListener("click", function () {
    const tipoData = document.getElementById("selectDataTipo").value;
    const mesSelecionado = document.getElementById("selectMes").value;

    if (mesSelecionado) {
        const url = `/filtrar_dividendos?tipo=${tipoData}&mes=${mesSelecionado}`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                const tabelaBody = document.querySelector("#tabelaDividendosFiltrados tbody");
                tabelaBody.innerHTML = ""; // Limpa o conteúdo anterior

                if (data.error) {
                    alert(data.error);
                    return;
                }

                // Preenche a tabela com os dados filtrados
                data.forEach(dividendo => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${dividendo.categoria}</td>
                        <td>${dividendo.tipo}</td>
                        <td>${dividendo.quantidade}</td>
                        <td>${dividendo.valor}</td>
                        <td>${dividendo.valor_total}</td>
                        <td>${dividendo.valor_total_liquido}</td>
                        <td>${dividendo.data_com}</td>
                        <td>${dividendo.data_pagamento}</td>
                    `;
                    tabelaBody.appendChild(row);
                });
            })
            .catch(error => {
                console.error("Erro ao filtrar dividendos:", error);
                alert("Ocorreu um erro ao filtrar os dividendos.");
            });
    } else {
        alert("Por favor, selecione um mês para filtrar.");
    }
});