import logging
import logging.handlers
import os
import time
from datetime import datetime
import telebot

from openai import OpenAI
from config import (
    API_TOKEN,
    API_KEY_PROXY,
    MAIL_USER,
    MAIL_APP_PASSWORD,
    MAIL_FROM,
    MAIL_TO,
)

# Настройка логирования
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Получаем текущую дату в формате YYYY-MM-DD
current_date = datetime.now().strftime("%Y-%m-%d")

logging.basicConfig(
    filename=os.path.join(LOG_DIR, f"chatgpt_bot_{current_date}.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
)

# Настройка обработчика для отправки критических сообщений по электронной почте
mail_handler = logging.handlers.SMTPHandler(
    mailhost=("smtp.gmail.com", 587),
    fromaddr=MAIL_FROM,
    toaddrs=[MAIL_TO],  # Отправка на адрес
    subject="Критическое сообщение журнала",
    credentials=(MAIL_USER, MAIL_APP_PASSWORD),
    secure=(),
)
mail_handler.setLevel(logging.CRITICAL)  # Уровень логирования для отправки по почте
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
mail_handler.setFormatter(formatter)

# Добавление обработчика к логгеру
logging.getLogger().addHandler(mail_handler)

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
            # {"role": "system", "content": "отвечай в неформальном стиле"}
            {"role": "system", "content": ""}
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
    logging.info("ChatGPT Bot запущен...")
    print("ChatGPT Bot запущен...")
    while True:
        try:
            bot.polling()
        except Exception as e:
            logging.critical(f"Критическая ошибка в работе бота: {str(e)}")
            time.sleep(5)
            continue
