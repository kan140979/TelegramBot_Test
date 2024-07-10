import re
import telebot
from config import API_TOKEN


bot = telebot.TeleBot(API_TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я ваш Telegram-бот. Чем могу помочь?")


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
    bot.reply_to(message, help_text)


# Обработчик команды /perevorot
@bot.message_handler(commands=["perevorot"])
def reverse_text(message):
    # Получаем текст после команды /perevorot
    text_to_reverse = message.text[len("/perevorot ") :]

    # Переворачиваем текст
    reversed_text = text_to_reverse[::-1]

    # Отправляем перевернутый текст обратно пользователю
    bot.reply_to(message, reversed_text)


# Обработчик команды /caps
@bot.message_handler(commands=["caps"])
def caps_text(message):
    # Получаем текст после команды /caps
    text_to_caps = message.text[len("/caps ") :]

    # Преобразуем текст в заглавные буквы
    caps_text = text_to_caps.upper()

    # Отправляем текст в заглавных буквах обратно пользователю
    bot.reply_to(message, caps_text)


# Обработчик команды /cut
@bot.message_handler(commands=["cut"])
def cut_vowels(message):
    # Получаем текст после команды /cut
    text_to_cut = message.text[len("/cut ") :]

    # Удаляем все гласные буквы
    vowels_pattern = r"[AEIOUaeiouАЕЁИОУЫЭЮЯаеёиоуыэюя]"
    cut_text = re.sub(vowels_pattern, "", text_to_cut)

    # Отправляем текст без гласных обратно пользователю
    bot.reply_to(message, cut_text)


# Обработчик команды /count
@bot.message_handler(commands=["count"])
def count_characters(message):
    # Получаем текст после команды /count
    text_to_count = message.text[len("/count ") :]

    # Подсчитываем количество символов
    char_count = len(text_to_count)

    # Отправляем количество символов обратно пользователю
    response = f"Количество символов: {char_count}"
    bot.reply_to(message, response)


# Основной цикл обработки сообщений
bot.polling()
