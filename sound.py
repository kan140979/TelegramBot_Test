# телеграмм бот отвечает голосом

import telebot
from openai import OpenAI
from config import API_TOKEN, API_KEY_PROXY
from gtts import gTTS
import os

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
    
    # Преобразование текста ответа в голосовое сообщение
    tts = gTTS(text=response, lang='ru')
    tts_file = f"voice_message_{user_id}.ogg"
    tts.save(tts_file)

    # Отправка голосового сообщения
    with open(tts_file, 'rb') as voice:
        bot.send_voice(message.chat.id, voice)
    
    # Удаление временного файла
    os.remove(tts_file)

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)