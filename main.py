import telebot

# Замените 'YOUR_API_TOKEN' на ваш реальный API токен, полученный у BotFather
API_TOKEN = "6888164226:AAExGsPcgA1WLAuwnpfd7D7YxDBTqW41rWg"

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message, "Привет! Я бот. Напиши 'Привет, бот!' или 'как дела?' чтобы получить ответ."
    )


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.lower() == "привет, бот!":
        bot.reply_to(message, "Привет, бот!")
    elif message.text.lower() == "как дела?":
        bot.reply_to(message, "Всё хорошо, спасибо!")
    else:
        bot.reply_to(message, "Извините, я вас не понимаю.")


if __name__ == "__main__":
    print("Бот запущен и готов к работе")
    bot.polling()
