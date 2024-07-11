# телеграмм бот отвечает нейросетью

import telebot
from openai import OpenAI
from config import API_TOKEN, API_KEY_PROXY

client = OpenAI(
    api_key=API_KEY_PROXY,
    base_url="https://api.proxyapi.ru/openai/v1",
)

bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения истории переписки для каждого пользователя
user_conversations = {}


def get_gpt_response(user_id, user_input):
    if user_id not in user_conversations:
        user_conversations[user_id] = []

    conversation_history = user_conversations[user_id]
    conversation_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106", messages=conversation_history
    )

    answer = response.choices[0].message.content
    conversation_history.append(
        {"role": "system", "content": "отвечай в научном стиле"}
    )

    return answer


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_input = message.text

    if user_input.lower() == "exit":
        bot.reply_to(message, "Завершение чата. До свидания!")
        if user_id in user_conversations:
            del user_conversations[user_id]
        return

    response = get_gpt_response(user_id, user_input)
    bot.reply_to(message, response)


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
