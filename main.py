# телеграмм бот с набором команд
import re
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import API_TOKEN

bot = telebot.TeleBot(API_TOKEN)

# Создаем кнопку "Действия" и клавиатуру
button_actions = KeyboardButton("Действия")
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(button_actions)


# Обработчик команды /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message, "Привет! Я ваш Telegram-бот. Чем могу помочь?", reply_markup=keyboard
    )


# Обработчик команды /help
@bot.message_handler(commands=["help"])
def send_help(message):
    help_text = (
        "Вот список команд, которые я поддерживаю:\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/perevorot <текст> - Перевернуть текст\n"
        "/caps <текст> - Преобразовать текст в заглавные буквы\n"
        "/cut <текст> - Удалить все гласные буквы из текста\n"
        "/count <текст> - Подсчитать количество символов в тексте"
    )
    bot.reply_to(message, help_text, reply_markup=keyboard)


# Обработчик нажатия кнопки "Действия"
@bot.message_handler(func=lambda message: message.text == "Действия")
def handle_actions(message):
    bot.reply_to(message, "Привет!")


# Обработчик команды /perevorot
@bot.message_handler(commands=["perevorot"])
def reverse_text(message):
    text_to_reverse = message.text[len("/perevorot ") :]
    reversed_text = text_to_reverse[::-1]
    bot.reply_to(message, reversed_text)


# Обработчик команды /caps
@bot.message_handler(commands=["caps"])
def caps_text(message):
    text_to_caps = message.text[len("/caps ") :]
    caps_text = text_to_caps.upper()
    bot.reply_to(message, caps_text)


# Обработчик команды /cut
@bot.message_handler(commands=["cut"])
def cut_vowels(message):
    text_to_cut = message.text[len("/cut ") :]
    vowels_pattern = r"[AEIOUaeiouАЕЁИОУЫЭЮЯаеёиоуыэюя]"
    cut_text = re.sub(vowels_pattern, "", text_to_cut)
    bot.reply_to(message, cut_text)


# Обработчик команды /count
@bot.message_handler(commands=["count"])
def count_characters(message):
    text_to_count = message.text[len("/count ") :]
    char_count = len(text_to_count)
    response = f"Количество символов: {char_count}"
    bot.reply_to(message, response)


# Основной цикл обработки сообщений
bot.polling()
