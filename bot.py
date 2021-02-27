# import telebot
# from message_text import *
from token_ import token_
# bot = telebot.TeleBot(token_, parse_mode=None)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def finish_get_choice(call):
#     print('Close')
#     bot.answer_callback_query(call.message.id, 'Ти нажав на Завершити!!')
#
#
# @bot.message_handler(commands=['start'])
# def start(message):
#     counter = 0
#     bot.send_message(message.chat.id, start_message,  reply_markup=create_keyboard())
#     # bot.register_next_step_handler(message, get_choice, counter)
#
#
#
# def get_choice(message, counter):
#     keyboard = create_keyboard() if counter > 0 else None
#     bot.send_message(message.chat.id, 'Зберіг!!', reply_markup=keyboard)
#     counter += 1
#     if counter < 14:
#         bot.register_next_step_handler(message, get_choice, counter)
#
#
# def create_keyboard():
#     keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     button = telebot.types.KeyboardButton('Завершити')
#     keyboard.add(button)
#     return keyboard
#
# @bot.callback_query_handler(func=lambda call: True)
# def finish_get_choice(call):
#     print('Close')
#     bot.answer_callback_query(call.id, 'Ти нажав на Завершити!!')
#
#
#
#
# bot.polling()

