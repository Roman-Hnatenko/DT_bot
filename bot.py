import telebot
from message_text import *
from token_ import token_
bot = telebot.TeleBot(token_, parse_mode=None)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, start_message)


bot.polling()
