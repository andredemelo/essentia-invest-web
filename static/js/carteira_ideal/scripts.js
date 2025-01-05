// Modais
const labels = Object.keys(alocacoesJson);
const data = Object.values(alocacoesJson);

        // Evento para abrir modal de edição com valores preenchidos
        $('#editarModal').on('show.bs.modal', function (event) {
            var button = $(event.relatedTarget);
            var classeAtivo = button.data('classe');
            var porcentagem = button.data('porcentagem');
            var dividendo_desejado = button.data('dividendo');

            var modal = $(this);
            modal.find('.modal-body #classe_ativo_modal_editar').val(classeAtivo);
            modal.find('.modal-body #porcentagem_modal_editar').val(porcentagem);
            modal.find('.modal-body #dividendo_desejado_editar').val(dividendo_desejado);
            modal.find('.modal-body #classe_ativo_hidden_editar').val(classeAtivo);
        });

        // Evento para abrir modal de exclusão com o valor correto
        $('#excluirModal').on('show.bs.modal', function (event) {
            var button = $(event.relatedTarget);
            var classeAtivo = button.data('classe');

            var modal = $(this);
            modal.find('#classe_ativo_modal_excluir').text(classeAtivo);
            modal.find('#classe_ativo_hidden_excluir').val(classeAtivo);
        });

// Gráfico de Pizza
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