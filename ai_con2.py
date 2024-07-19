import logging
import os
import telebot
from openai import OpenAI
from config import API_TOKEN, API_KEY_PROXY

# Настройка логирования
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename=os.path.join(log_dir, "bot.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding='utf-8'
)

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

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106", messages=conversation_history
        )
        answer = response.choices[0].message.content
        conversation_history.append(
            {"role": "system", "content": "отвечай в деловом стиле"}
        )
        logging.info(f"Ответ для пользователя {user_id}: {answer}")
        return answer
    except Exception as e:
        logging.error(
            f"Ошибка при получении ответа от модели для пользователя {user_id}: {str(e)}"
        )
        return "Произошла ошибка при обращении к модели. Пожалуйста, попробуйте позже."


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_input = message.text
    logging.info(f"Получено сообщение от пользователя {user_id}: {user_input}")

    if user_input.lower() == "exit":
        bot.reply_to(message, "Завершение чата. До свидания!")
        if user_id in user_conversations:
            del user_conversations[user_id]
        logging.info(f"Чат с пользователем {user_id} завершен")
        return

    response = get_gpt_response(user_id, user_input)
    bot.reply_to(message, response)


if __name__ == "__main__":
    logging.info("Бот запущен...")
    print("Бот запущен...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.critical(f"Критическая ошибка в работе бота: {str(e)}")
