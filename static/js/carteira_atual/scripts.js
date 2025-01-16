// Preenche o modal com os dados do ativo selecionado
$('#modalPrecoJusto').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Botão que acionou o modal
    var ticker = button.data('ticker'); // Dados do ativo
    var precoAtual = button.data('preco-atual');
    var precoBazin = button.data('preco-bazin');
    var precoGraham = button.data('preco-graham');

    // Atualiza o conteúdo do modal
    var modal = $(this);
    modal.find('#modalTicker').text(ticker);
    modal.find('#modalPrecoAtual').text(precoAtual.toFixed(2));
    modal.find('#modalPrecoBazin').text(precoBazin.toFixed(2));
    modal.find('#modalPrecoGraham').text(precoGraham.toFixed(2));
});