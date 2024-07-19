import telebot
from telebot import types
import json
from config import API_TOKEN

# Вставьте ваш токен бота

bot = telebot.TeleBot(API_TOKEN)

# Вопросы для опроса
questions = ["Как вас зовут?", "Сколько вам лет?", "Какой ваш любимый цвет?"]

# Хранилище для ответов пользователей
user_responses = {}


# Начало опроса
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот для проведения опросов. Начнем?")
    send_question(message.chat.id, 0)


# Отправка вопроса
def send_question(chat_id, question_index):
    if question_index < len(questions):
        question = questions[question_index]
        msg = bot.send_message(chat_id, question)
        bot.register_next_step_handler(
            msg, lambda message: save_response(message, question_index)
        )
    else:
        bot.send_message(chat_id, "Спасибо за участие в опросе!")
        save_results(chat_id)


# Сохранение ответа и переход к следующему вопросу
def save_response(message, question_index):
    chat_id = message.chat.id
    if chat_id not in user_responses:
        user_responses[chat_id] = []

    user_responses[chat_id].append(message.text)
    send_question(chat_id, question_index + 1)


# Сохранение результатов опроса в файл
def save_results(chat_id):
    with open("survey_results.json", "w", encoding="utf-8") as f:
        json.dump(user_responses, f, ensure_ascii=False, indent=4)
    bot.send_message(chat_id, "Ваши ответы сохранены. Спасибо!")


# Команда для просмотра результатов опроса (доступна только администратору)
@bot.message_handler(commands=["results"])
def send_results(message):
    if message.chat.id == int("328703575"):  # Замените на ваш Telegram ID
        with open("survey_results.json", "r", encoding="utf-8") as f:
            results = json.load(f)
            bot.send_message(
                message.chat.id, json.dumps(results, ensure_ascii=False, indent=4)
            )
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к результатам.")


# Запуск бота
bot.polling(none_stop=True)
