import requests
import logging

# 🧠 История сообщений по каждому пользователю
user_histories = {}

def ask_ollama(prompt: str, user_id: int, model: str = "gemma3:4b") -> str:
    history = user_histories.get(user_id, [])
    history.append({"role": "user", "content": prompt})

    # 💡 Ограничим историю последними 10 сообщениями
    history = history[-10:]
    user_histories[user_id] = history

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": model,
                "messages": history,
                "stream": False
            }
        )
        response.raise_for_status()
        data = response.json()

        answer = data["message"]["content"]
        history.append({"role": "assistant", "content": answer})
        user_histories[user_id] = history

        return answer
    except requests.RequestException as e:
        logging.error(f"Ошибка при запросе к Ollama API: {e}")
        return "⚠️ Ошибка при общении с нейросетью."

