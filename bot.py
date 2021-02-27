import telebot
from message_text import *
from token_ import token_
bot = telebot.TeleBot(token_, parse_mode=None)


@bot.callback_query_handler(func=lambda call: True)
def finish_get_choice(call):
    print('Close')
    bot.answer_callback_query(call.message.id, 'Ти нажав на Завершити!!')


@bot.message_handler(commands=['start'])
def start(message):
    counter = 0
    bot.send_message(message.chat.id, start_message, )
    bot.register_next_step_handler(message, get_choice, counter)


def get_choice(message, counter):
    counter += 1
    try:
        keyboard = create_keyboard() if counter > 2 else None
        if message.text.lower() == 'завершити':
            bot.send_message(message.chat.id, 'Ти нажав на Завершити!!', reply_markup=telebot.types.ReplyKeyboardRemove())
            raise ValueError

        bot.send_message(message.chat.id, 'Зберіг!!', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_choice, counter)

    except Exception:
        pass


def create_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = telebot.types.KeyboardButton('Завершити')
    keyboard.add(button)
    return keyboard


@bot.message_handler(content_types=['text'])
def finish_get_choice(message):
    if message.text.lowwer() == 'завершити':
        print('Close')
        bot.send_message(message.chat.id, 'Ти нажав на Завершити!!')

bot.polling()

