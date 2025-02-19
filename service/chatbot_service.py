from flask import Flask, request, jsonify
import requests

def chat_chatbot():
    data = request.get_json()
    user_message = data.get("message")

    # Enviar mensagem para a API do Llama via Ollama
    llama_response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": user_message, "stream": False}
    )

    try:
        bot_response = llama_response.json()  # Converte a resposta para JSON
    except requests.exceptions.JSONDecodeError:
        bot_response = {"error": "Erro ao processar a resposta da IA."}

    return jsonify({"response": bot_response["response"]})
