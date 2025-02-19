document.addEventListener("DOMContentLoaded", function () {
    const chatButton = document.getElementById("chat-button");
    const chatModal = document.getElementById("chat-modal");
    const closeChat = document.getElementById("close-chat");
    const sendChat = document.getElementById("send-chat");
    const chatInput = document.getElementById("chat-input");
    const chatBody = document.getElementById("chat-body");

    // Exibir/Ocultar o chat
    chatButton.addEventListener("click", () => {
        chatModal.style.display = "flex";
    });

    closeChat.addEventListener("click", () => {
        chatModal.style.display = "none";
    });

    // Enviar mensagem para a API
    sendChat.addEventListener("click", async () => {
        let userMessage = chatInput.value.trim();
        if (userMessage === "") return;

        // Adicionar mensagem do usuário no chat
        chatBody.innerHTML += `<p class="user-message">${userMessage}</p>`;
        chatInput.value = "";

        // Chamar a API do Llama via Flask
        let response = await fetch("/chatbot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage })
        });

        let data = await response.json();

        // Adicionar resposta do bot no chat
        chatBody.innerHTML += `<p class="bot-message">${data.response}</p>`;

        // Rolar para a última mensagem
        chatBody.scrollTop = chatBody.scrollHeight;
    });
});